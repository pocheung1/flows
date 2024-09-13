from flytekit import workflow
from flytekit.types.directory import FlyteDirectory
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask


@workflow
def workflow() -> FlyteDirectory:
    """
    pyflyte run --remote output_flyte_directory_workflow.py workflow
    """

    task = DominoJobTask(
        name="FlyteDirectory Output Task",
        domino_job_config=DominoJobConfig(
            Command="python output_flyte_directory.py",
        ),
        inputs={},
        outputs={'output_path': FlyteDirectory},
        use_latest=True,
    )()

    print(f"FlyteDirectory: {task['output_path']}")
    return task['output_path']
