from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, DatasetSnapshot
from flytekitplugins.domino.helpers import run_domino_job_task


@workflow
def workflow() -> None:
    """
    pyflyte run --remote dataset_workflow.py workflow
    """

    run_domino_job_task(
        flyte_task_name="Shared datasets",
        # command="cat /mnt/data/foo/version.txt /mnt/imported/data/flows-playground/version.txt",
        command="ls -lR /mnt/data /mnt/imported/data",
        dataset_snapshots=[
            # Success
            # Dataset missing id and name
            DatasetSnapshot(Version=1),
            # Dataset snapshot version 0
            DatasetSnapshot(Id="66b31d987fb95b3989a25d0f", Name="foo", Version=0),
            # Warning: no version provided
            # DatasetSnapshot(Id="66b31d987fb95b3989a25d0f"),
            # Dataset name mismatch
            DatasetSnapshot(Id="66b31d987fb95b3989a25d0f", Name="bad"),
            # Dataset snapshot not found
            DatasetSnapshot(Id="bad-id"),
            # Dataset snapshot not found
            DatasetSnapshot(Name="bad-name"),
            # Dataset does not have any snapshots
            DatasetSnapshot(Name="no-snapshot"),
            # Dataset snapshot version 99 not found.
            DatasetSnapshot(Id="66b31d987fb95b3989a25d0f", Version=99),
            # Dataset id mismatch
            DatasetSnapshot(Id="bad-id", Name="foo"),
            # Multiple datasets match by name and version
            DatasetSnapshot(Name="foo", Version=1),
            # Multiple datasets match by name
            DatasetSnapshot(Name="foo"),
            # Multiple snapshots for the same dataset
            DatasetSnapshot(Id="66a589d607325c0ea95729dd", Name="flows-playground", Version=1),
            DatasetSnapshot(Id="66a589d607325c0ea95729dd", Name="flows-playground", Version=2),
        ],
        use_project_defaults_for_omitted=True
    )
