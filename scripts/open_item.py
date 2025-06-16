import sys
import os
import json
import subprocess
import urllib.parse
import utils

# get tag & uid from env vars
tag=os.environ["tag"]
uid=os.environ["uid"]
print(f"tag={tag}\nuid={uid}", file=sys.stderr)

# load items.json
data_path = os.path.join(os.environ["alfred_workflow_data"], "items.json")
with open(data_path) as f:
    data = json.load(f)

# find the right block & entry
block = next((b for b in data if b.get("tag") == tag), {})
entry = next((e for e in block.get("items", []) if e.get("uid") == uid), {})

# decide how to open

item_type = entry.get("type", "")
if item_type == "email":
    message_id = entry.get("id", "")
    encoded = urllib.parse.quote(f"<{message_id}>")
    subprocess.run(["open", f"message://{encoded}"])

elif item_type == "file":
    path = entry.get("path", "")
    subprocess.run(["open", path])

elif item_type == "webpage":
    url = entry.get("url", "")
    browser = os.environ.get("browser")
    subprocess.run(["open", "-a", browser, url])

# add to recent list/file
utils.add_to_recent(entry, tag)
