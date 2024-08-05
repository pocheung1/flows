from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, DatasetSnapshot


@workflow
def workflow() -> None:
    """
    pyflyte run --remote dataset_workflow.py workflow
    """

    DominoJobTask(
        name="Dataset",
        domino_job_config=DominoJobConfig(
            Command="cat /mnt/data/snapshots/flows/2/hello.txt",
            DatasetSanpshots=[
                DatasetSnapshot(Id="66b15adb4c11b830fac3fe57", Name="flows", Version=1),
                DatasetSnapshot(Id="66b15b0c4c11b830fac3fe5b", Name="flows", Version=2),
            ],
        ),
        use_latest=True,
    )()
