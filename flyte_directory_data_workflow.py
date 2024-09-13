from flytekit import workflow
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import CSVFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask


@workflow
def workflow(data_path: str) -> CSVFile:
    """
    Example to illustrate using FlyteDirectory as task input and output.

    The first task:
    - accepts a CSV file path as input
    - reads the CSV file into a DataFrame
    - extracts each column in the DataFrame into a CSV file
    - outputs a FlyteDirectory that contains the CSV files
    
    The second task:
    - accepts a FlyteDirectory as input
    - reads the CSV files from the FlyteDirectory path
    - sums the values in each row across the column in each CSV file
    - writes a CSV file containing the sums as named output

    To run this workflow, execute the following line in the terminal:

    pyflyte run --remote flyte_directory_data_workflow.py workflow --data_path /mnt/code/data/data.csv

    :param data_path: Path of the CSV data file
    :return: CSV file containing the sums
    """

    data_prep_task = DominoJobTask(
        name="Prepare data",
        domino_job_config=DominoJobConfig(
            Command="python flyte_directory_data_prep.py",
        ),
        inputs={'data_path': str},
        outputs={'csv_files': FlyteDirectory},
        use_latest=True,
    )
    data_prep_results = data_prep_task(data_path=data_path)

    data_process_task = DominoJobTask(
        name="Process data",
        domino_job_config=DominoJobConfig(
            Command="python flyte_directory_data_process.py",
        ),
        inputs={
            'csv_files': FlyteDirectory,
            'epochs': int,
            'batch_size': int,
        },
        outputs={
            'sum': CSVFile,
        },
        use_latest=True,
    )
    data_process_results = data_process_task(
        csv_files=data_prep_results['csv_files'],
        epochs=10,
        batch_size=32,
    )

    return data_process_results['sum']
