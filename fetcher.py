import os
from github import Github, Auth
from dotenv import load_dotenv


load_dotenv()


def get_pr_diff(pr_url):
    token = os.getenv("GITHUB_TOKEN")
    from github import Auth
    auth = Auth.Token(token)
    g = Github(auth=auth)

    # Parse the PR URL
    # Example URL: https://github.com/owner/repo/pull/123
    parts = pr_url.strip("/").split("/")
    owner = parts[3]
    repo_name = parts[4]
    pr_number = int(parts[6])

    repo = g.get_repo(f"{owner}/{repo_name}")
    pr = repo.get_pull(pr_number)

    files = pr.get_files()

    diff_text = ""
    for f in files:
        diff_text += f"\n--- File: {f.filename} ---\n"
        if f.patch:
            diff_text += f.patch

    return {
        "title": pr.title,
        "author": pr.user.login,
        "files_changed": pr.changed_files,
        "diff": diff_text
    }


if __name__ == "__main__":
    url = input("Paste a GitHub PR URL: ")
    result = get_pr_diff(url)
    print(f"\nPR Title: {result['title']}")
    print(f"Author: {result['author']}")
    print(f"Files changed: {result['files_changed']}")
    print(f"\nDiff preview (first 500 chars):\n{result['diff'][:500]}")