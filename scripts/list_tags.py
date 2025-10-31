import os
import json
import sys
import utils

query_raw = sys.argv[1] if len(sys.argv) > 1 else ""
query = utils.normalize_symbols(query_raw.lower()) if query_raw and query_raw != "(null)" else ""

workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")

# Load data
if not os.path.exists(items_path):
    print(json.dumps({ "items": [] }))
    exit(0)

with open(items_path, "r") as f:
    data = json.load(f)

# Build tag summary
items = []
for block in data:
    tag = block.get("tag", "")
    type_counts = { "email":0, "file":0, "webpage":0}

    for item in block.get("items", []):
        t = item.get("type")
        if t in type_counts:
            type_counts[t] += 1

    # Skip tags with no items
    if not any(type_counts.values()):
        continue

    # Build summary string like: [2 emails, 4 webpage, 1 file]
    type_labels = []
    if type_counts["email"]:
        type_labels.append(f'{type_counts["email"]} email{"s" if type_counts["email"] > 1 else ""}')
    if type_counts["webpage"]:
        type_labels.append(f'{type_counts["webpage"]} webpage{"s" if type_counts["webpage"] > 1 else ""}')
    if type_counts["file"]:
        type_labels.append(f'{type_counts["file"]} file{"s" if type_counts["file"] > 1 else ""}')

    subtitle = f"[{', '.join(type_labels)}] • ↵ View types • ⌘ Rename • ⌥ Remove • ⌃ View all"

    #override icon is special tag is specified
    icon = utils.get_icon_for_tag(tag)

    # perform search
    terms = query.split()
    if query and not all(term in tag.lower() for term in terms):
        continue

    items.append({
        "title": tag,
        "subtitle": subtitle,
        "arg": tag,
        "icon": icon,
        "mods": {
            "cmd": {
                "subtitle": "⌘ Rename tag",
                "arg": tag,
                "variables": {
                    "old_tag": tag
                }
            },
            "alt": {
                "subtitle": "⌥ Remove tag",
                "arg": tag
            },
            "ctrl": {
                "subtitle": "⌃ View items",
                "arg": tag
            }
        }
    })

# If no items matched, show fallback
if not items:
    items.append({
        "title": "No matches found",
        "subtitle": "So then tag some, silly",
        "valid": False,
        "icon": { "path": "info.png" }
    })
else:
    total = len(items)
    items.insert(0, {
        "title": f"{total} tagged groups",
        "valid": False,
        "icon": { "path": "info.png" }
    })

items.sort(key=lambda x: x["title"].lower())
print(json.dumps({ "items": items }))
