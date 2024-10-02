from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask


@workflow
def workflow() -> None:
    """
    pyflyte run --remote simple_workflow.py workflow
    """

    DominoJobTask(
        name="Sleep",
        domino_job_config=DominoJobConfig(
            Command="sleep 60",
        ),
        use_latest=True,
    )()
