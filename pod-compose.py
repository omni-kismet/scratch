import os
import sys
import subprocess

# Function to build a Docker image using either Docker or Podman, given a tool, Dockerfile path, and image name
def build_image(tool, dockerfile_path, image_name):
    cmd = [tool, "build", "-t", image_name, "-f", dockerfile_path, "."]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Image '{image_name}' built successfully using {tool}.")
        return image_name
    else:
        print(f"Failed to build the image '{image_name}' using {tool}.")
        print(result.stderr)
        return None

def create_container(tool, image_name, container_name):
    cmd = [tool, "run", "--name", container_name, "-d", image_name]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Created and started container '{container_name}' using {tool}.")
        return container_name
    else:
        print(f"Failed to create and start container '{container_name}' using {tool}.")
        print(result.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python build_containers.py docker|podman /path/to/dockerfile_directory [-r]")
        sys.exit(1)

    tool = sys.argv[1].lower()
    dockerfile_directory = sys.argv[2]
    run_containers_flag = "-r" in sys.argv[3:]

    if tool not in ["docker", "podman"]:
        print("Invalid tool specified. Please use 'docker' or 'podman'.")
        sys.exit(1)

    for root, _, files in os.walk(dockerfile_directory):
        for file in files:
            if file.startswith("Dockerfile."):
                dockerfile_path = os.path.join(root, file)
                image_name = os.path.splitext(file)[1][1:].lower()
                built_image_name = build_image(tool, dockerfile_path, image_name)

                if run_containers_flag and built_image_name:
                    container_name = f"{image_name}-container"
                    create_container(tool, built_image_name, container_name)
