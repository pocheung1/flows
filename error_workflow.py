from flytekit import workflow
from flytekitplugins.domino.helpers import run_domino_job_task
from flytekitplugins.domino.task import DatasetSnapshot, GitRef, ExternalDataVolume


@workflow
def workflow() -> None:
    """
    pyflyte run --remote error_workflow.py workflow
    """

    run_domino_job_task(
        flyte_task_name="Error handling task",
        command="echo error_workflow",
        main_git_repo_ref=GitRef("head2"),
        volume_size_gib=1,
        environment_name="bad_environment_name",
        hardware_tier_name="bad_hardware_tier_name",
        dataset_snapshots=[
            # Dataset missing id and name
            DatasetSnapshot(Version=1),
            # Dataset snapshot not found by id
            DatasetSnapshot(Id="bad_dataset_id"),
            # Dataset snapshot not found by name
            DatasetSnapshot(Name="bad_dataset_name"),
            # Dataset snapshot version must be greater than 0
            DatasetSnapshot(Name="flows", Version=0),
            # Dataset snapshot version 99 not found
            DatasetSnapshot(Name="flows", Version=99),
        ],
        external_data_volumes=[
            ExternalDataVolume(Name="bad_edv_name"),
        ],
        use_project_defaults_for_omitted=False,
    )
