from utils.flyte import DominoTask, Output
from flytekit import workflow
from flytekit.types.file import FlyteFile


@workflow
def workflow() -> FlyteFile:
    """
    To run this workflow: pyflyte run --remote basic_workflow.py workflow
    """

    results = DominoTask(
        name="Basic workflow",
        command="python /mnt/code/model.py",
        environment="V2 Flyte Env",
        hardware_tier="Small",
        inputs=[],
        outputs=[
            Output(name="model", type=FlyteFile)
        ]
    )

    return results['model']
