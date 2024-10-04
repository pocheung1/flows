from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask


@workflow
def workflow() -> FlyteFile["json"]:
    """
    pyflyte run --remote output_json_workflow.py workflow
    """

    results = DominoJobTask(
        name="JSON Output Task",
        domino_job_config=DominoJobConfig(
            Command="python output_json.py",
        ),
        inputs={},
        outputs={'model': FlyteFile["json"]},
        use_latest=True,
    )()

    return results['model']
