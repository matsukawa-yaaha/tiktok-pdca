#!/usr/bin/env python3
"""Postiz API wrapper for TikTok PDCA automation."""

import sys
import json
import os
import requests

CONFIG_PATH = os.path.expanduser("~/.claude/tiktok-pdca/config.json")


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def get_headers(api_key):
    return {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }


def cmd_integrations(base_url, api_key):
    """List all connected channels/integrations."""
    resp = requests.get(f"{base_url}/integrations", headers=get_headers(api_key))
    resp.raise_for_status()
    data = resp.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_analytics(base_url, api_key, integration_id, days=7):
    """Get analytics for an integration."""
    resp = requests.get(
        f"{base_url}/analytics/{integration_id}",
        headers=get_headers(api_key),
        params={"date": days},
    )
    resp.raise_for_status()
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))


def cmd_upload(base_url, api_key, file_path):
    """Upload a local image file to Postiz."""
    headers = {"Authorization": api_key}
    with open(file_path, "rb") as f:
        resp = requests.post(
            f"{base_url}/upload",
            headers=headers,
            files={"file": (os.path.basename(file_path), f, "image/png")},
        )
    resp.raise_for_status()
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))


def cmd_create_draft(base_url, api_key):
    """Create a draft post. Reads JSON from stdin.

    Expected stdin JSON:
    {
      "integration_id": "...",
      "content": "...",
      "date": "2026-03-26T10:00:00.000Z",  // optional, defaults to today 19:00 JST
      "images": [{"id": "...", "path": "..."}]
    }
    """
    from datetime import datetime, timezone, timedelta

    data = json.loads(sys.stdin.read())
    integration_id = data["integration_id"]
    content = data["content"]
    images = data.get("images", [])

    # Default: today at 19:00 JST (= 10:00 UTC)
    if "date" in data:
        post_date = data["date"]
    else:
        jst = timezone(timedelta(hours=9))
        today = datetime.now(jst).replace(hour=19, minute=0, second=0, microsecond=0)
        post_date = today.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    payload = {
        "type": "schedule",
        "date": post_date,
        "shortLink": False,
        "tags": [],
        "posts": [
            {
                "integration": {"id": integration_id},
                "value": [
                    {
                        "content": content,
                        "image": [{"id": img["id"], "path": img["path"]} for img in images],
                    }
                ],
                "settings": {
                    "__type": "tiktok",
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                    "duet": False,
                    "stitch": False,
                    "comment": True,
                    "autoAddMusic": "no",
                    "brand_content_toggle": False,
                    "brand_organic_toggle": False,
                    "content_posting_method": "UPLOAD",
                },
            }
        ],
    }

    resp = requests.post(f"{base_url}/posts", headers=get_headers(api_key), json=payload)
    resp.raise_for_status()
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))


def main():
    config = load_config()
    base_url = config["postiz_base_url"]
    api_key = config["postiz_api_key"]

    if len(sys.argv) < 2:
        print("Usage: postiz_api.py <command> [args]")
        print("Commands: integrations | analytics <id> [days] | upload <file> | create_draft")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "integrations":
        cmd_integrations(base_url, api_key)

    elif cmd == "analytics":
        if len(sys.argv) < 3:
            print("Usage: postiz_api.py analytics <integration_id> [days]", file=sys.stderr)
            sys.exit(1)
        integration_id = sys.argv[2]
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        cmd_analytics(base_url, api_key, integration_id, days)

    elif cmd == "upload":
        if len(sys.argv) < 3:
            print("Usage: postiz_api.py upload <file_path>", file=sys.stderr)
            sys.exit(1)
        cmd_upload(base_url, api_key, sys.argv[2])

    elif cmd == "create_draft":
        cmd_create_draft(base_url, api_key)

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
