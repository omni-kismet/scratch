# Dockerfile Builder

This script builds Docker images from Dockerfiles located in a specified directory using Podman. The script also has an option to create and run containers from the built images.

## Requirements

- Python 3.6 or higher
- Podman installed and configured on your system

## Usage

To run the script, use the following command:
``sh
python compose.py /path/to/dockerfile_directory [-c]
``

- `/path/to/dockerfile_directory`: The path to the directory containing Dockerfiles with extensions (e.g., `Dockerfile.sample1`, `Dockerfile.sample2`).
- `-c`: (Optional) If this flag is provided, the script will create and run containers from the built images.

## How it works

1. The script iterates through the specified directory and its subdirectories to find Dockerfiles with extensions.
2. For each Dockerfile found, the script builds a Docker image using Podman and tags it with the file's extension (e.g., `sample1` for `Dockerfile.sample1`).
3. If the `-c` flag is provided, the script creates and runs a container for each built image using Podman.

## Example

Suppose you have the following directory structure:

dockerfiles/
|- Dockerfile.sample1
|- Dockerfile.sample2

To build images from these Dockerfiles and run containers from the images, run the following command:

python build_containers.py dockerfiles -c

The script will build the images and create containers named `sample1-container` and `sample2-container`.

