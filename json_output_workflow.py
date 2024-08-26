from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask
from typing import TypeVar


@workflow
def workflow() -> FlyteFile:
    """
    pyflyte run --remote json_output_workflow.py workflow
    """

    results = DominoJobTask(
        name="JSON Output Workflow",
        domino_job_config=DominoJobConfig(
            Command="python json_output.py",
        ),
        inputs={},
        outputs={'model': FlyteFile[TypeVar("json")]},
        use_latest=True,
    )()

    return results['model']
