import requests
import json
import time

VLLM_URL = "http://localhost:8080/v1/completions"
MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"


def review_chunk(chunk, chunk_index):
    prompt = f"""You are an expert code reviewer. Analyze the following code diff and identify issues.

Respond only with valid JSON in this exact format:
{{"issues": [{{"severity": "high/medium/low", "line_reference": "filename or line", "issue": "description", "suggestion": "how to fix it"}}], "summary": "one sentence summary"}}

If no issues found, return {{"issues": [], "summary": "No issues found."}}

Code diff:
{chunk}

JSON response:"""

    start_time = time.time()
    try:
        response = requests.post(VLLM_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "max_tokens": 500,
            "temperature": 0.1
        }, timeout=60)
        elapsed = time.time() - start_time
        print(f"  [Chunk {chunk_index}] Inference time: {elapsed:.2f}s")
        result = response.json()
        raw_text = result["choices"][0]["text"].strip()
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        if start != -1 and end > start:
            parsed = json.loads(raw_text[start:end])
            return parsed
        return {"issues": [], "summary": raw_text[:200]}
    except Exception as e:
        return {"issues": [], "summary": f"Error: {str(e)}"}
