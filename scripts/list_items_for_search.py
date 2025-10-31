#!/usr/bin/env python3

import os
import sys
import json
import urllib.parse
import utils

query = utils.normalize_symbols(sys.argv[1].strip().lower()) if len(sys.argv) > 1 else ""
raw_query = query

use_or = False
if query.endswith(":or"):
    use_or = True
    query = query[:-3].strip()

print(f"QUERY: {query}", file=sys.stderr)

workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")

if not os.path.exists(items_path):
    print(json.dumps({ "items": [] }))
    exit(0)

with open(items_path, "r") as f:
    tag_groups = json.load(f)

# Start items list, include save option if query exists
items = []
if raw_query:
    items.append({
        "title": "Save this search",
        "subtitle": "↵ to Save this search",
        "arg": raw_query,
        "icon": { "path": "save.png" },
        "variables": {
            "action": "save_search"
        }
    })


webpage_icon = utils.get_webpage_icon()

for group in tag_groups:
    tag = group.get("tag", "")

    for item in group.get("items", []):

        fields = utils.get_item_fields(item, tag, webpage_icon)
        if not fields:
            continue

        item_type = fields["item_type"]
        uid = fields["uid"]
        title = fields["title"]
        subtitle = fields["subtitle"]
        path = fields["path"]
        icon = fields["icon"]

        terms = query.split()
        search_fields = [tag, title, item_type, subtitle]

        if query:
            if use_or:
                if not any(term in (f or "").lower() for term in terms for f in search_fields):
                    continue
            else:
                if not all(any(term in (f or "").lower() for f in search_fields) for term in terms):
                    continue

        subtitle = f"[{tag}] • [{item_type}] • {subtitle}"

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

if len(items) == 1:
    items.append({
        "title": "No matches found",
        "subtitle": "Maybe next time",
        "valid": False,
        "icon": { "path": "info.png" }
    })
else:
    total = len(items) - 1
    items.insert(0, {
        "title": f"{total} tagged items",
        "valid": False,
        "icon": { "path": "info.png" }
    })

print(json.dumps({ "items": items }))
