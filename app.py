import gradio as gr
from main import review_pr
import json


def run_review(pr_url):
    if not pr_url.strip():
        return "Please paste a GitHub PR URL first."

    try:
        report = review_pr(pr_url)

        output = f"## PR Review: {report['pr_title']}\n"
        output += f"**Author:** {report['author']}\n"
        output += f"**Files Changed:** {report['files_changed']}\n"
        output += f"**Total Issues Found:** {report['total_issues']}\n\n"

        if report['issues']:
            output += "---\n## Issues\n\n"
            for issue in report['issues']:
                severity = issue.get('severity', 'unknown').upper()

                # Color code by severity
                if severity == 'HIGH':
                    emoji = "🔴"
                elif severity == 'MEDIUM':
                    emoji = "🟡"
                else:
                    emoji = "🟢"

                output += f"{emoji} **[{severity}]** `{issue.get('line_reference', 'N/A')}`\n"
                output += f"**Problem:** {issue.get('issue', 'N/A')}\n"
                output += f"**Fix:** {issue.get('suggestion', 'N/A')}\n\n"
        else:
            output += "---\n## No issues found in this PR.\n"

        output += "---\n## Chunk Summaries\n"
        for i, summary in enumerate(report['chunk_summaries']):
            output += f"- **Chunk {i + 1}:** {summary}\n"

        return output

    except Exception as e:
        return f"Error: {str(e)}\n\nMake sure the PR URL is public and valid."



with gr.Blocks(title="CodeEnforcer") as demo:
    gr.Markdown("# CodeEnforcer\nAI-powered GitHub PR reviewer running on AMD MI300X GPU")

    with gr.Row():
        pr_input = gr.Textbox(
            label="GitHub PR URL",
            placeholder="https://github.com/owner/repo/pull/123",
            scale=4
        )
        submit_btn = gr.Button("Review PR", variant="primary", scale=1)

    output_box = gr.Markdown(label="Review Results")

    submit_btn.click(
        fn=run_review,
        inputs=pr_input,
        outputs=output_box
    )

    gr.Examples(
        examples=["https://github.com/pallets/flask/pull/5650"],
        inputs=pr_input
    )


if __name__ == "__main__":
    demo.launch()