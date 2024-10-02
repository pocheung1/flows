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


@workflow
def workflow() -> FlyteDirectory:
    # Generate a directory with files
    return create_files()
