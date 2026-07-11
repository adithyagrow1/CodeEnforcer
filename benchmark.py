import time
import requests
import json

VLLM_URL = "http://localhost:8080/v1/completions"
MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"

test_diff = """--- File: auth.py ---
+def authenticate(user, password):
     if user == None:
         return False
+    query = f"SELECT * FROM users WHERE username = {user}"
+    print("Password: " + password)
"""

def benchmark_gpu(runs=5):
    times = []
    for i in range(runs):
        start = time.time()
        response = requests.post(VLLM_URL, json={
            "model": MODEL_NAME,
            "prompt": f"Review this code diff:\n{test_diff}\nRespond with JSON.",
            "max_tokens": 200,
            "temperature": 0.1
        }, timeout=60)
        elapsed = time.time() - start
        times.append(elapsed)
        tokens = response.json()["usage"]["completion_tokens"]
        print(f"  Run {i+1}: {elapsed:.2f}s | {tokens} tokens | {tokens/elapsed:.1f} tokens/sec")
    
    avg = sum(times) / len(times)
    print(f"\nAverage inference time: {avg:.2f}s")
    print(f"Min: {min(times):.2f}s | Max: {max(times):.2f}s")
    return avg

print("=== CodeEnforcer GPU Benchmark ===")
print(f"Model: {MODEL_NAME}")
print(f"Hardware: AMD Instinct MI300X (192GB VRAM)")
print(f"Software: vLLM on ROCm 7.2")
print()
print("Running 5 inference calls...")
avg = benchmark_gpu(5)

results = {
    "model": MODEL_NAME,
    "hardware": "AMD Instinct MI300X",
    "vram": "192GB",
    "rocm_version": "7.2",
    "average_inference_time_seconds": round(avg, 2),
    "use_case": "GitHub PR code review"
}

with open("benchmark_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to benchmark_results.json")
