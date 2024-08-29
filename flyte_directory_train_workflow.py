from flytekit import workflow
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import CSVFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask


@workflow
def workflow(data_path: str) -> CSVFile:
    """
    Example to illustrate using FlyteDirectory as task input and output.

    The first task:
    - accepts a data directory path as input
    - outputs that as a FlyteDirectory
    
    The second task:
    - accepts a FlyteDirectory as input
    - reads the CSV files from the FlyteDirectory path
    - sums the values in each row across the column in each CSV file
    - writes a CSV file containing the sums

    To run this workflow, execute the following line in the terminal:

    pyflyte run --remote flyte_directory_train_workflow.py workflow --data_path /mnt/code/data

    :param data_path: Path of the data directory
    :return: CSV file containing the sums
    """

    prepare_data = DominoJobTask(
        name="Prepare data",
        domino_job_config=DominoJobConfig(
            Command="python flyte_directory_train_data_prep.py",
        ),
        inputs={'data_path': str},
        outputs={'data_dir': FlyteDirectory},
        use_latest=True,
    )
    prepare_data_results = prepare_data(data_path=data_path)

    train_model = DominoJobTask(
        name="Train model",
        domino_job_config=DominoJobConfig(
            Command="python flyte_directory_train_model.py",
        ),
        inputs={
            'data_dir': FlyteDirectory,
            'epochs': int,
            'batch_size': int,
        },
        outputs={
            'sum': CSVFile,
        },
        use_latest=True,
    )
    train_model_results = train_model(
        data_dir=prepare_data_results['data_dir'],
        epochs=10,
        batch_size=32,
    )

    return train_model_results['sum']
