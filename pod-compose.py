import os
import sys
import subprocess

# Function to build a Docker image using either Docker or Podman, given a tool, Dockerfile path, and image name
def build_image(tool, dockerfile_path, image_name):
    # Construct the Docker or Podman build command
    cmd = [tool, "build", "-t", image_name, "-f", dockerfile_path, "."]

    # Execute the build command and capture the output
    result = subprocess.run(cmd, capture_output=True, text=True)

    # If the build is successful, print a success message and return the image name
    if result.returncode == 0:
        print(f"Image '{image_name}' built successfully using {tool}.")
        return image_name
    else:
        # If the build fails, print an error message and the stderr output, then return None
        print(f"Failed to build the image '{image_name}' using {tool}.")
        print(result.stderr)
        return None

# Function to create and start a container using either Docker or Podman, given a tool, image name, and container name
def create_container(tool, image_name, container_name):
    # Construct the Docker or Podman run command
    cmd = [tool, "run", "--name", container_name, "-d", image_name]

    # Execute the run command and capture the output
    result = subprocess.run(cmd, capture_output=True, text=True)

    # If the container creation is successful, print a success message and return the container name
    if result.returncode == 0:
        print(f"Created and started container '{container_name}' using {tool}.")
        return container_name
    else:
        # If the container creation fails, print an error message and the stderr output, then return None
        print(f"Failed to create and start container '{container_name}' using {tool}.")
        print(result.stderr)
        return None

# Main script execution
if __name__ == "__main__":
    # Check if the required command-line arguments are provided
    if len(sys.argv) < 4:
        print("Usage: python build_containers.py docker|podman /path/to/dockerfile_directory [-r]")
        sys.exit(1)

    # Parse the command-line arguments
    tool = sys.argv[1].lower()
    dockerfile_directory = sys.argv[2]
    run_containers_flag = "-r" in sys.argv[3:]

    # Check if a valid tool is provided
    if tool not in ["docker", "podman"]:
        print("Invalid tool specified. Please use 'docker' or 'podman'.")
        sys.exit(1)

    # Iterate through the Dockerfile directory and its subdirectories
    for root, _, files in os.walk(dockerfile_directory):
        # Iterate through the files in the current directory
        for file in files:
            # If the file is a Dockerfile with an extension
            if file.startswith("Dockerfile."):
                # Construct the full Dockerfile path
                dockerfile_path = os.path.join(root, file)
                # Extract the image name from the file extension
                image_name = os.path.splitext(file)[1][1:].lower()
                # Build the image using the Dockerfile
                built_image_name = build_image(tool, dockerfile_path, image_name)

                # If the '-r' flag is provided and the
