from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask
from typing import TypeVar


@workflow
def workflow() -> None:
    """
    pyflyte run --remote input_txt_workflow.py workflow
    """

    DominoJobTask(
        name="Text Input Task",
        domino_job_config=DominoJobConfig(
            Command="python input_txt.py",
        ),
        inputs={'model': FlyteFile[TypeVar("txt")]},
        outputs={},
        use_latest=True,
    )()
