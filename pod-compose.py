import os
import sys
import fnmatch
import subprocess

def build_image(dockerfile_path, image_name):
    cmd = ["podman", "build", "-t", image_name, "-f", dockerfile_path, "."]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Image '{image_name}' built successfully.")
        return image_name
    else:
        print(f"Failed to build the image '{image_name}'.")
        print(result.stderr)
        return None

def create_container(image_name, container_name):
    cmd = ["podman", "run", "--name", container_name, "-d", image_name]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Created and started container '{container_name}'.")
        return container_name
    else:
        print(f"Failed to create and start container '{container_name}'.")
        print(result.stderr)
        return None

def build_and_run_containers(directory, create_containers=False):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith("Dockerfile."):
                dockerfile_path = os.path.join(root, file)
                image_name = os.path.splitext(file)[1][1:].lower()
                built_image_name = build_image(dockerfile_path, image_name)

                if create_containers and built_image_name:
                    container_name = f"{image_name}-container"
                    create_container(built_image_name, container_name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_containers.py /path/to/dockerfile_directory [-c]")
        sys.exit(1)

    directory = sys.argv[1]
    create_containers_flag = "-c" in sys.argv[2:]

    build_and_run_containers(directory, create_containers=create_containers_flag)
