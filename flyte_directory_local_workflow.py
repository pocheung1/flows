import os
from pathlib import Path

import flytekit
from flytekit import task, workflow
from flytekit.types.directory import FlyteDirectory


@task(enable_deck=True)
def create_files() -> FlyteDirectory:
    working_dir = flytekit.current_context().working_directory
    local_dir = Path(working_dir) / "txt_files"
    local_dir.mkdir(exist_ok=True)
    print(f"Local directory: {local_dir}")

    # Create multiple text files in the directory
    for i in range(3):
        file_path = os.path.join(local_dir, f"file_{i}.txt")
        with open(file_path, "w") as f:
            f.write(f"Content of file {i}")

    return FlyteDirectory(local_dir)


@task
def create_directory() -> FlyteDirectory:
    # Create an empty FlyteDirectory object that points to a temporary directory
    output_dir = FlyteDirectory.create_at("my_output_directory")

    # Use the new_file method to create files inside the directory
    for i in range(3):
        file_path = os.path.join(output_dir.path, f"file_{i}.txt")
        with output_dir.new_file(file_path, mode="w") as f:
            f.write(f"Content of file {i}\n")

    # Return the FlyteDirectory object with files
    return output_dir


@workflow
def workflow() -> FlyteDirectory:
    # Generate a directory with files
    return create_files()
