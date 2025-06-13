import os
import sys
import json
import urllib.parse
import utils

query = utils.normalize_symbols(sys.argv[1].strip().lower()) if len(sys.argv) > 1 else ""

print(f"QUERY: {query}", file=sys.stderr)

workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")

if not os.path.exists(items_path):
    print(json.dumps({ "items": [] }))
    exit(0)

with open(items_path, "r") as f:
    tag_groups = json.load(f)

items = [{}]
#items = [{
#    "title": "Keyboard shortcuts",
#    "subtitle": "↵ Open • ⌘ Remove item • ⌥ Rename title",
#    "valid": False,
#    "icon": { "path": "info.png" }
#}]

bookmark_icon = utils.get_bookmark_icon()

for group in tag_groups:
    tag = group.get("tag", "")

    for item in group.get("items", []):

        # get fields for this item
        fields = utils.get_item_fields(item, tag, bookmark_icon)
        if not fields:
            continue

        item_type = fields["item_type"]
        uid = fields["uid"]
        title = fields["title"]
        subtitle = fields["subtitle"]
        path = fields["path"]
        icon = fields["icon"]

        # perform search
        terms = query.split()
        if not all(
            any(term in (x or "").lower() for x in [tag, title, item_type, subtitle])
            for term in terms
        ):
            continue

        subtitle = f"[{tag}] • {subtitle}"

        #override icon is special tag is specified
        custom_icon = utils.get_icon_for_tag(title, subtitle)
        if custom_icon != "":
            icon = custom_icon

        items.append({
            "title": title,
            "subtitle": subtitle,
            "arg": path,
            "icon": icon,
            "variables": {
                "tag": tag,
                "uid": uid,
                "caller": "search_tags"
            },
            "mods": {
                "cmd": {
                    "subtitle": "⌘ Remove item",
                    "arg": f"{tag}||{uid}",
                    "variables": {
                        "caller": "search_tags"
                    }
                },
                "alt": {
                    "subtitle": "⌥ Rename title",
                    "arg": title,
                    "variables": {
                        "tag": tag,
                        "uid": uid,
                        "old_title": title,
                        "caller": "search_tags"
                }
              }
            }
        })

# Fallback if no match
if len(items) == 1:
    items = [{
        "title": "No matches found",
        "subtitle": "So tag some!",
        "valid": False,
        "icon": { "path": "info.png" }
    }]

print(json.dumps({ "items": items }))
