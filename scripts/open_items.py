import os
import sys
import json
import subprocess
import urllib.parse
import utils

# Args
tag, item_type = [utils.normalize_symbols(x.strip()) for x in sys.argv[1].split("||")]

# Paths
workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")

# Load items
if not os.path.exists(items_path):
    sys.exit(0)

with open(items_path, "r") as f:
    data = json.load(f)

# Find tag block
block = next((b for b in data if b.get("tag") == tag), None)
if not block:
    sys.exit(0)

# Open each matching item
for item in block.get("items", []):
    if item.get("type") != item_type:
        continue

    if item_type == "file":
        path = item.get("path")
        if path and os.path.exists(path):
            subprocess.run(["open", path])

    elif item_type == "webpage":
        url = item.get("url")
        if url:
            browser = os.environ.get("browser")
            subprocess.run(["open", "-a", browser, url])

    elif item_type == "email":
        message_id = item.get("id")
        if message_id:
            encoded = urllib.parse.quote(f"<{message_id}>")
            subprocess.run(["open", f"message://{encoded}"])

