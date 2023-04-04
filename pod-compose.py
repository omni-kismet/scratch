import os
import sys
import fnmatch
import subprocess

# Function to build a Docker image using Podman, given a Dockerfile path and image name
def build_image(dockerfile_path, image_name):
    # Construct the Podman build command
    cmd = ["podman", "build", "-t", image_name, "-f", dockerfile_path, "."]
    
    # Execute the Podman build command and capture the output
    result = subprocess.run(cmd, capture_output=True, text=True)

    # If the build is successful, print a success message and return the image name
    if result.returncode == 0:
        print(f"Image '{image_name}' built successfully.")
        return image_name
    else:
        # If the build fails, print an error message and the stderr output, then return None
        print(f"Failed to build the image '{image_name}'.")
        print(result.stderr)
        return None

# Function to create and start a container from an image using Podman, given an image name and container name
def create_container(image_name, container_name):
    # Construct the Podman run command
    cmd = ["podman", "run", "--name", container_name, "-d", image_name]
    
    # Execute the Podman run command and capture the output
    result = subprocess.run(cmd, capture_output=True, text=True)

    # If the container creation is successful, print a success message and return the container name
    if result.returncode == 0:
        print(f"Created and started container '{container_name}'.")
        return container_name
    else:
        # If the container creation fails, print an error message and the stderr output, then return None
        print(f"Failed to create and start container '{container_name}'.")
        print(result.stderr)
        return None

# Function to build and run containers given a directory containing Dockerfiles and a flag indicating whether to create containers
def build_and_run_containers(directory, create_containers=False):
    # Iterate through the directory and its subdirectories
    for root, _, files in os.walk(directory):
        # Iterate through the files in the current directory
        for file in files:
            # If the file is a Dockerfile with an extension
            if file.startswith("Dockerfile."):
                # Construct the full Dockerfile path
                dockerfile_path = os.path.join(root, file)
                # Extract the image name from the file extension
                image_name = os.path.splitext(file)[1][1:].lower()
                # Build the image using the Dockerfile
                built_image_name = build_image(dockerfile_path, image_name)

                # If the '-c' flag is set and the image was built successfully, create and run a container
                if create_containers and built_image_name:
                    container_name = f"{image_name}-container"
                    create_container(built_image_name, container_name)

# Main script execution
if __name__ == "__main__":
    # If the script is called without the required arguments, print the usage message and exit
    if len(sys.argv) < 2:
        print("Usage: python build_containers.py /path/to/dockerfile_directory [-c]")
        sys.exit(1)

    # Parse the command-line arguments
    directory = sys.argv[1]
    create_containers_flag = "-c" in sys.argv[2:]

    # Call the build_and_run_containers function with the parsed arguments
    build_and_run_containers(directory, create_containers=create_containers_flag)
