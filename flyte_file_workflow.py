from flytekit import task, workflow
from flytekit.types.file import FlyteFile


@task
def generate_file() -> FlyteFile:
    output_path = "/tmp/flyte_file_workflow_output.txt"
    with open(output_path, "w") as output:
        print("This is the workflow output", file=output)

    return FlyteFile(output_path)


@workflow
def workflow() -> FlyteFile:
    """
    pyflyte run --remote flyte_file_workflow.py workflow
    """
    return generate_file()


# Execute workflow
if __name__ == "__main__":
    ex = workflow()
    print(ex)
