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

bookmark_icon = utils.get_bookmark_icon()

for entry in recent:
    uid = entry.get("uid")
    tag = entry.get("tag", "")

    if uid not in valid_uids:
        continue  # skip if item no longer exists

    # get fields for this item
    fields = utils.get_item_fields(entry, tag, bookmark_icon)
    if not fields:
        continue

    item_type = fields["item_type"]
    title = fields["title"]
    subtitle = fields["subtitle"]
    path = fields["path"]
    icon = fields["icon"]

    # apply filtering
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

    updated_recent.append(entry)  # keep valid item in recent.json

# Overwrite recent.json with only valid entries
with open(recent_path, "w") as f:
    json.dump(updated_recent, f, indent=2)

# No results fallback
if not items:
    items = [{
        "title": "Nothing here yet",
        "subtitle": "But there will be soon 🤪",
        "valid": False,
        "icon": { "path": "info.png" }
    }]

print(json.dumps({ "items": items }))

