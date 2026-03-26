#!/usr/bin/env python3
"""OpenAI image generation for TikTok PDCA automation."""

import sys
import json
import os
import base64

CONFIG_PATH = os.path.expanduser("~/.claude/tiktok-pdca/config.json")
TMP_DIR = "/tmp"


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def generate_image(prompt: str, index: int = 0) -> dict:
    """Generate an image using the configured OpenAI model.

    Returns:
        {"file_path": "/tmp/tiktok_pdca_image_{index}.png"}
    """
    try:
        from openai import OpenAI
    except ImportError:
        print(json.dumps({"error": "openai package not installed. Run: pip install openai"}))
        sys.exit(1)

    config = load_config()
    client = OpenAI(api_key=config["openai_api_key"])
    model = config.get("image_model", "gpt-image-1")
    size = config.get("image_size", "1024x1536")

    response = client.images.generate(
        model=model,
        prompt=prompt,
        n=1,
        size=size,
        quality="high",
    )

    file_path = os.path.join(TMP_DIR, f"tiktok_pdca_image_{index}.png")

    item = response.data[0]
    if getattr(item, "b64_json", None):
        image_bytes = base64.b64decode(item.b64_json)
        with open(file_path, "wb") as f:
            f.write(image_bytes)
    elif getattr(item, "url", None):
        import urllib.request
        urllib.request.urlretrieve(item.url, file_path)
    else:
        print(json.dumps({"error": "No image data in response"}))
        sys.exit(1)

    return {"file_path": file_path}


def main():
    if len(sys.argv) < 2:
        print("Usage: openai_api.py generate <prompt> [index]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "generate":
        if len(sys.argv) < 3:
            print("Usage: openai_api.py generate <prompt> [index]", file=sys.stderr)
            sys.exit(1)
        prompt = sys.argv[2]
        index = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        result = generate_image(prompt, index)
        print(json.dumps(result))

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
