from utils.flyte import DominoTask
from flytekit import workflow


@workflow
def workflow() -> None:
    """
    To run this workflow: pyflyte run --remote sleep_workflow.py workflow
    """

    DominoTask(
        name="Sleep workflow",
        command="python /mnt/code/sleep.py",
        environment="V2 Flyte Env",
        hardware_tier="Small",
        inputs=[],
        outputs=[],
    )
