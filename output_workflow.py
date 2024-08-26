from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask
from typing import TypeVar

@workflow
def workflow() -> FlyteFile:
    """
    pyflyte run --remote output_workflow.py workflow
    """

    results = DominoJobTask(
        name="Output workflow test",
        domino_job_config=DominoJobConfig(
            Command="python output.py",
        ),
        inputs={},
        outputs={'model': FlyteFile[TypeVar("txt")]},
        use_latest=True,
    )()

    return results['model']
