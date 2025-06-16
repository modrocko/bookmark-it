import os
import sys
import json
import urllib.parse
import utils

query = utils.normalize_symbols(sys.argv[1].strip().lower()) if len(sys.argv) > 1 else ""
terms = query.split()

workflow_data = os.environ["alfred_workflow_data"]
recent_path = os.path.join(workflow_data, "recent.json")
items_path = os.path.join(workflow_data, "items.json")

# Load recent.json
try:
    with open(recent_path) as f:
        recent = json.load(f)
except FileNotFoundError:
    recent = []

# Load items.json
try:
    with open(items_path) as f:
        tag_groups = json.load(f)
except FileNotFoundError:
    tag_groups = []

# Build set of valid uids
valid_uids = {
    item["uid"]
    for group in tag_groups
    for item in group.get("items", [])
}

items = []
updated_recent = []
webpage_icon = utils.get_webpage_icon()

for entry in recent:
    uid = entry.get("uid")
    tag = entry.get("tag", "")

    if uid not in valid_uids:
        continue  # ❌ Skip if item no longer exists

    ############################
    #skip the file type if it no longeer exists on disk

    fields = utils.get_item_fields(entry, tag, webpage_icon)
    if not fields:
        continue

    # ❌ Skip file items if the file is gone
    if fields["item_type"] == "file" and not os.path.exists(fields["path"]):
        continue
    ############################

    updated_recent.append(entry)  # ✅ Keep all valid entries (entries that also exising in main data file)

    fields = utils.get_item_fields(entry, tag, webpage_icon)
    if not fields:
        continue

    item_type = fields["item_type"]
    title = fields["title"]
    subtitle = fields["subtitle"]
    path = fields["path"]
    icon = fields["icon"]

    if terms and not all(
        any(term in (x or "").lower() for x in [tag, title, item_type, subtitle])
        for term in terms
    ):
        continue

    subtitle = f"[{tag}] • {subtitle}"

    items.append({
        "title": title,
        "subtitle": subtitle,
        "arg": path,
        "icon": icon,
        "variables": {
            "tag": tag,
            "uid": uid
        }
    })

# Save only valid entries back to recent.json
with open(recent_path, "w") as f:
    json.dump(updated_recent, f, indent=2)

# Fallback message
if not items:
    items = [{
        "title": "Nothing here yet",
        "subtitle": "But there will be soon 🤪",
        "valid": False,
        "icon": { "path": "info.png" }
    }]

print(json.dumps({ "items": items }))
