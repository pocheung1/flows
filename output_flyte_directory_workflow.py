from flytekit import workflow
from flytekit.types.directory import FlyteDirectory
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask


@workflow
def workflow() -> FlyteDirectory:
    """
    pyflyte run --remote output_flyte_directory_workflow.py workflow
    """

    results = DominoJobTask(
        name="FlyteDirectory Output Task",
        domino_job_config=DominoJobConfig(
            Command="python output_flyte_directory.py",
        ),
        inputs={},
        outputs={'model': FlyteDirectory},
        use_latest=True,
    )()

    return results['model']
