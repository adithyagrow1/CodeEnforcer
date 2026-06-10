import requests
import json

# This will point to your GPU instance later
# For now it points to localhost for testing

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-coder:6.7b"


def review_chunk(chunk, chunk_index):
    prompt = f"""You are an expert code reviewer. Analyze the following code diff and identify issues.

For each issue found, respond in this exact JSON format:
{{
  "issues": [
    {{
      "severity": "high/medium/low",
      "line_reference": "approximate line or file",
      "issue": "description of the problem",
      "suggestion": "how to fix it"
    }}
  ],
  "summary": "one sentence summary of this chunk"
}}

If no issues found, return {{"issues": [], "summary": "No issues found in this chunk."}}

Code diff to review:
{chunk}

Respond only with valid JSON, nothing else."""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }, timeout=60)

        result = response.json()
        raw_text = result.get("response", "")

        # Parse the JSON response from LLM
        parsed = json.loads(raw_text)
        return parsed

    except requests.exceptions.ConnectionError:
        # GPU instance not running yet — return placeholder
        print(f"  [Chunk {chunk_index}] GPU instance not connected yet, using placeholder")
        return {
            "issues": [
                {
                    "severity": "medium",
                    "line_reference": "placeholder",
                    "issue": "GPU instance not connected — this will be real output once MI300X is running",
                    "suggestion": "Connect to AMD Developer Cloud instance"
                }
            ],
            "summary": "Placeholder review — GPU instance not connected yet."
        }
    except json.JSONDecodeError:
        return {
            "issues": [],
            "summary": f"Could not parse LLM response for chunk {chunk_index}"
        }


if __name__ == "__main__":
    test_chunk = """--- File: auth.py ---
+def authenticate(user, password):
-def authenticate(user, pwd):
     if user == None:
         return False
+    query = f"SELECT * FROM users WHERE username = {user}"
"""
    print("Testing reviewer...")
    result = review_chunk(test_chunk, 1)
    print(json.dumps(result, indent=2))