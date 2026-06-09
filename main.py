# CodeEnforcer - AI PR Review Agent
from fetcher import get_pr_diff
from chunker import chunk_diff
from reviewer import review_chunk
import json


#io
def review_pr(pr_url):
    print(f"\nFetching PR: {pr_url}")
    pr_data = get_pr_diff(pr_url)

    print(f"Title: {pr_data['title']}")
    print(f"Author: {pr_data['author']}")
    print(f"Files changed: {pr_data['files_changed']}")

    print(f"\nChunking diff...")
    chunks = chunk_diff(pr_data['diff'])
    print(f"Total chunks to review: {len(chunks)}")

    all_issues = []
    summaries = []

    for i, chunk in enumerate(chunks):
        print(f"Reviewing chunk {i + 1}/{len(chunks)}...")
        result = review_chunk(chunk, i + 1)
        all_issues.extend(result.get("issues", []))
        summaries.append(result.get("summary", ""))

    # Sort issues by severity
    severity_order = {"high": 0, "medium": 1, "low": 2}
    all_issues.sort(key=lambda x: severity_order.get(x.get("severity", "low"), 2))

    final_report = {
        "pr_title": pr_data['title'],
        "author": pr_data['author'],
        "files_changed": pr_data['files_changed'],
        "total_issues": len(all_issues),
        "issues": all_issues,
        "chunk_summaries": summaries
    }

    return final_report



if __name__ == "__main__":
    url = input("Paste a GitHub PR URL: ")
    report = review_pr(url)

    print("\n" + "=" * 50)
    print("REVIEW COMPLETE")
    print("=" * 50)
    print(f"PR: {report['pr_title']}")
    print(f"Total issues found: {report['total_issues']}")

    if report['issues']:
        print("\nISSUES:")
        for issue in report['issues']:
            print(f"\n[{issue['severity'].upper()}] {issue['line_reference']}")
            print(f"  Problem: {issue['issue']}")
            print(f"  Fix: {issue['suggestion']}")

    print("\nSUMMARIES:")
    for i, s in enumerate(report['chunk_summaries']):
        print(f"  Chunk {i + 1}: {s}")