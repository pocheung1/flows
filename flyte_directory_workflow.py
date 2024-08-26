from flytekit import workflow
from flytekit.types.directory import FlyteDirectory
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask


@workflow
def workflow() -> FlyteDirectory:
    """
    pyflyte run --remote flyte_directory_workflow.py workflow
    """

    results = DominoJobTask(
        name="Output workflow test",
        domino_job_config=DominoJobConfig(
            Command="python flyte_directory_output.py",
        ),
        inputs={},
        outputs={'model': FlyteDirectory},
        use_latest=True,
    )()

    return results['model']
