def chunk_diff(diff_text, max_chars=3000):
    chunks = []
    current_chunk = ""

    lines = diff_text.split("\n")

    for line in lines:
        # If adding this line would exceed max_chars, save current chunk and start new one
        if len(current_chunk) + len(line) > max_chars:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    # Don't forget the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


if __name__ == "__main__":
    # Test with fake diff text
    test_diff = """--- File: app.py ---
+def login(user, password):
-def login(user, pwd):
    if not user:
        return None
""" * 20  # repeat it to simulate a large diff

    chunks = chunk_diff(test_diff)
    print(f"Total chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i + 1} ({len(chunk)} chars) ---")
        print(chunk[:200])