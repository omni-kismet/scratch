import subprocess
import argparse


def clean_podman():
    # Clean all existing podman containers and images
    subprocess.run(["podman", "rm", "-a", "-f"], capture_output=True)
    subprocess.run(["podman", "rmi", "-a", "-f"], capture_output=True)
    print("All podman containers and images have been deleted.")


def list_podman():
    # List all existing podman containers and images
    containers_output = subprocess.run(["podman", "ps", "-a", "--format", "table {{.Names}}\t{{.Image}}\t{{.ID}}"],
                                       capture_output=True, text=True)
    images_output = subprocess.run(["podman", "images", "--format", "table {{.Repository}}\t{{.Tag}}\t{{.ID}}"],
                                   capture_output=True, text=True)
    print("Existing podman containers:")
    print(containers_output.stdout)
    print("Existing podman images:")
    print(images_output.stdout)


def main():
    parser = argparse.ArgumentParser(description="Clean or list podman containers and images.")
    parser.add_argument("--clean", action="store_true", help="Delete all podman containers and images.")
    parser.add_argument("--report", action="store_true", help="List all podman containers and images.")
    args = parser.parse_args()

    if args.clean:
        clean_podman()

    if args.report:
        list_podman()


if __name__ == "__main__":
    main()
