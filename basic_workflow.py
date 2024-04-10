from utils.flyte import DominoTask
from flytekit import workflow


@workflow
def workflow() -> None:
    """
    To run this workflow: pyflyte run --remote basic_workflow.py workflow
    """

    DominoTask(
        name="Basic workflow",
        command="python /mnt/code/job.py",
        environment="V2 Flyte Env",
        hardware_tier="Small",
        inputs=[],
        outputs=[],
    )
