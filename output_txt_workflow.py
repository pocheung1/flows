from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask


@workflow
def workflow() -> FlyteFile["txt"]:
    """
    pyflyte run --remote output_txt_workflow.py workflow
    """

    results = DominoJobTask(
        name="Text Output Task",
        domino_job_config=DominoJobConfig(
            Command="python output_txt.py",
        ),
        inputs={},
        outputs={'model': FlyteFile["txt"]},
        use_latest=True,
    )()

    return results['model']
