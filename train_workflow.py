from utils.flyte import DominoTask, Input, Output
from flytekit import workflow
from flytekit.types.file import FlyteFile


@workflow
def workflow(data_path: str) -> FlyteFile:
    """
    Sample data preparation and training workflow

    This workflow accepts a path to a CSV for some initial input and simulates
    the processing of the data and usage of the processed data in a training job.

    To run this workflowp, execute the following line in the terminal

    pyflyte run --remote train_workflow.py workflow --data_path /mnt/code/data/data.csv

    :param data_path: Path of the CSV file data
    :return: The training results as a model
    """

    data_prep_results = DominoTask(
        name="Prepare data",
        command="python /mnt/code/train_data_prep.py",
        environment="V2 Flyte Env",
        hardware_tier="Small",
        inputs=[
            Input(name="data_path", type=str, value=data_path)
        ],
        outputs=[
            Output(name="processed_data", type=FlyteFile)
        ]
    )

    training_results = DominoTask(
        name="Train model",
        command="python /mnt/code/train_model.py",
        environment="V2 Flyte Env",
        hardware_tier="Small",
        inputs=[
            Input(name="processed_data", type=FlyteFile, value=data_prep_results['processed_data']),
            Input(name="epochs", type=int, value=10),
            Input(name="batch_size", type=int, value=32)
        ],
        outputs=[
            Output(name="model", type=FlyteFile)
        ]
    )

    return training_results['model']
