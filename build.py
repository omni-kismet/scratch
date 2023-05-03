import os
import sys
import argparse
import subprocess
import shutil
from git import Repo
import paramiko

def parse_arguments():
    parser = argparse.ArgumentParser(description='Git checkout and build artifacts.')
    parser.add_argument('-r', '--repo', required=True, help='GitLab repository URL')
    parser.add_argument('-b', '--branch', default='master', help='Branch to checkout')
    parser.add_argument('-c', '--commit_repo', required=True, help='Commit repository URL')
    parser.add_argument('-m', '--commit_message', default='Add built artifacts', help='Commit message')
    parser.add_argument('-t', '--tag', help='Tag name for the commit')
    parser.add_argument('--gitlab_host', default='gitlab.com', help='GitLab host URL')
    parser.add_argument('--ssh_key', help='Path to SSH private key')
    parser.add_argument('--cleanup', action='store_true', help='Clean up the cloned repository after commit')

    return parser.parse_args()

def setup_ssh_auth(ssh_key):
    ssh_agent = paramiko.Agent()
    if ssh_key:
        key = paramiko.RSAKey.from_private_key_file(ssh_key)
        ssh_agent.add_key(key)
    else:
        ssh_agent.add_keys(ssh_agent.get_keys())

def git_checkout_and_build(args):
    try:
        print(f"Cloning {args.repo} ({args.branch})...")
        repo = Repo.clone_from(args.repo, "source_repo", branch=args.branch, env={'GIT_SSH_COMMAND': 'ssh -o StrictHostKeyChecking=no'})

        print("Running './gradlew izpack'...")
        result = subprocess.run(['./gradlew', 'izpack'], cwd="source_repo", capture_output=True, text=True)
        if result.returncode != 0:
            print("Error building artifacts:")
            print(result.stderr)
            sys.exit(1)
        else:
            print("Artifacts built successfully.")
            print(result.stdout)
    except Exception as e:
        print(f"Error during Git checkout or build: {e}")
        sys.exit(1)

    return repo

def commit_built_artifacts(args, source_repo):
    try:
        print(f"Cloning {args.commit_repo}...")
        commit_repo = Repo.clone_from(args.commit_repo, "commit_repo", env={'GIT_SSH_COMMAND': 'ssh -o StrictHostKeyChecking=no'})

        print("Adding built artifacts (jar and xml files)...")
        for root, _, files in os.walk("source_repo"):
            for file in files:
                if file.endswith('.jar') or file.endswith('.xml'):
                    source_path = os.path.join(root, file)
                    target_path = os.path.join("commit_repo", file)
                    os.replace(source_path, target_path)

        commit_repo.git.add(A=True)
        commit_repo.git.commit(m=args.commit_message)

        if args.tag:
            print(f"Tagging commit with tag '{args.tag}'")
            commit_repo.git.tag(args.tag)

        print("Pushing commit to repository...")
        commit_repo.git.push(tags=True)
        print("Commit pushed successfully.")
    except Exception as e:
        print(f"Error during commit or push: {e}")
        sys.exit(1)

    if args.cleanup:
        print("Cleaning up cloned repositories...")
        shutil.rmtree("source_repo")
        shutil.rmtree("commit_repo")

def main():
    args = parse_arguments()
    setup_ssh_auth(args.ssh_key)
    source_repo = git_checkout_and_build(args)
    commit_built_artifacts(args, source_repo)

if __name__ == "__main__":
    main()
