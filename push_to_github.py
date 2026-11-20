"""Helper script to push refactored OsdagBridge code to GitHub.

Usage:
    python push_to_github.py [remote_url]

Examples:
    python push_to_github.py https://github.com/<your-username>/OsdagBridge.git
"""
import sys
import os

try:
    from dulwich import porcelain
    from dulwich.repo import Repo
except ImportError:
    print("Error: dulwich library not found. Install via: pip install dulwich")
    sys.exit(1)

repo_path = os.path.dirname(os.path.abspath(__file__))

def main():
    repo = Repo(repo_path)
    print(f"Repository at: {repo_path}")
    
    # Check current branch
    head = repo.head()
    print(f"HEAD commit: {head.decode() if isinstance(head, bytes) else head}")
    
    if len(sys.argv) > 1:
        remote_url = sys.argv[1].strip()
        print(f"Setting remote 'origin' to: {remote_url}")
        try:
            porcelain.remote_add(repo_path, 'origin', remote_url)
        except Exception:
            # Update existing
            config = repo.get_config()
            config.set(('remote', 'origin'), 'url', remote_url.encode())
            config.write_to_path()
            print("Updated remote 'origin' URL.")

    # Show remotes
    config = repo.get_config()
    try:
        url = config.get(('remote', 'origin'), 'url').decode()
        print(f"Target remote URL: {url}")
    except KeyError:
        print("No 'origin' remote configured yet. Please pass your fork URL: python push_to_github.py https://github.com/<user>/OsdagBridge.git")
        return

    print("\nTo push, run with your GitHub token / credentials or standard git:")
    print("  git push -u origin dev")
    print("\nOr using dulwich:")
    try:
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            print("GITHUB_TOKEN found in environment. Pushing to origin/dev...")
            porcelain.push(repo_path, 'origin', 'refs/heads/dev:refs/heads/dev')
            print("Successfully pushed to GitHub!")
        else:
            print("Set GITHUB_TOKEN environment variable to push automatically via this script, or use standard git CLI.")
    except Exception as exc:
        print(f"Push attempt: {exc}")

if __name__ == "__main__":
    main()
