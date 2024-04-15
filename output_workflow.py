from utils.flyte import DominoTask, Output
from flytekit import workflow
from flytekit.types.file import FlyteFile


@workflow
def workflow() -> FlyteFile:
    """
    pyflyte run --remote output_workflow.py workflow
    """

    results = DominoTask(
        name="Output workflow",
        command="python /mnt/code/output.py",
        environment="V2 Flyte Env",
        hardware_tier="Small",
        inputs=[],
        outputs=[
            Output(name="model", type=FlyteFile)
        ]
    )

    return results['model']
