import os
import sys
import json
import urllib.parse
import utils

query = sys.argv[1].strip().replace("!", "❗").lower() if len(sys.argv) > 1 else ""

workflow_data = os.environ["alfred_workflow_data"]
recent_path = os.path.join(workflow_data, "recent.json")

try:
    with open(recent_path) as f:
        recent = json.load(f)
except FileNotFoundError:
    recent = []

items = []

bookmark_icon = utils.get_bookmark_icon()

for entry in recent:
    tag = entry.get("tag", "")

    # get fields for this item
    fields = utils.get_item_fields(entry, tag, bookmark_icon)
    if not fields:
        continue

    item_type = fields["item_type"]
    uid = fields["uid"]
    title = fields["title"]
    subtitle = fields["subtitle"]
    path = fields["path"]
    icon = fields["icon"]

    terms = query.split()
    if not all(
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

# No results fallback
if not items:
    items = [{
        "title": "Nothing here yet",
        "subtitle": "But there will be soon 🤪",
        "valid": False,
        "icon": { "path": "info.png" }
    }]

print(json.dumps({ "items": items }))
