from flytekit import workflow
from flytekit.types.directory import FlyteDirectory
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask


@workflow
def workflow() -> None:
    """
    pyflyte run --remote input_flyte_directory_workflow.py workflow
    """

    DominoJobTask(
        name="FlyteDirectory Input Task",
        domino_job_config=DominoJobConfig(
            Command="python input_flyte_directory.py",
        ),
        inputs={'model': FlyteDirectory},
        outputs={},
        use_latest=True,
    )()
