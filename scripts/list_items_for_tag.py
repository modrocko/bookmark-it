import os
import sys
import json
import urllib.parse
import utils

# Get incoming values
query_tag = utils.normalize_symbols(sys.argv[1].split("||")[-1].strip())

filter_type = os.environ.get("item_type")

print("filter type:", filter_type, file=sys.stderr)

# Set up paths
workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")
workflow_dir_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

webpage_icon = utils.get_webpage_icon()

# Load tagged data
if not os.path.exists(items_path):
    print(json.dumps({ "items": [] }))
    exit(0)

with open(items_path, "r") as f:
    data = json.load(f)

# Find tag block
block = next((b for b in data if b.get("tag") == query_tag), None)
if not block or not block.get("items"):
    print(json.dumps({ "items": [] }))
    exit(0)

items = []
for entry in block["items"]:

    # get fields for this item
    fields = utils.get_item_fields(entry, query_tag, webpage_icon)
    if not fields:
        continue

    item_type = fields["item_type"]
    uid = fields["uid"]
    title = fields["title"]
    subtitle = fields["subtitle"]
    path = fields["path"]
    icon = fields["icon"]

    if filter_type and filter_type != "all" and item_type != filter_type:
        continue

    items.append({
        "uid": uid,
        "title": title,
        "subtitle": subtitle,
        "arg": path,
        "icon": icon,
        "variables": {
            "tag": query_tag,
            "uid": uid,
            "caller": "list_items"
        },
        "mods": {
            "cmd": {
                "subtitle": "⌘ Remove item",
                "arg": f"{query_tag}||{uid}",
                "variables": {
                    "caller": "list_items"
                }
            },
            "alt": {
                "subtitle": "⌥ Rename title",
                "arg": title,
                "variables": {
                    "tag": query_tag,
                    "uid": uid,
                    "old_title": title,
                    "caller": "list_items"
                }
              }
            }
        })


items.sort(key=lambda x: x["title"].lower())

print(json.dumps({ "items": items }))
