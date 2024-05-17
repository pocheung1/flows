from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef


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

    prepare_data = DominoJobTask(
        name="Prepare data",
        domino_job_config=DominoJobConfig(
            Command="python train_data_prep.py",
            MainRepoGitRef=GitRef("head"),
        ),
        inputs={'data_path': str},
        outputs={'processed_data': FlyteFile},
        use_latest=True,
    )
    prepare_data_results = prepare_data(data_path=data_path)

    train_model = DominoJobTask(
        name="Train model",
        domino_job_config=DominoJobConfig(
            Command="python train_model.py",
            MainRepoGitRef=GitRef("head"),
        ),
        inputs={
            'data': FlyteFile,
            'epochs': int,
            'batch_size': int,
        },
        outputs={
            'model': FlyteFile,
        },
        use_latest=True,
    )
    train_model_results = train_model(
        data=prepare_data_results['processed_data'],
        epochs=10,
        batch_size=32,
    )

    return train_model_results['model']
