#!/usr/bin/env python3

import os
import sys
import json
import subprocess

query = sys.argv[1].strip() if len(sys.argv) > 1 else ""
if not query:
    sys.exit(0)

workflow_dir = os.environ.get("alfred_workflow_data")
workflow_name = os.environ.get("alfred_workflow_name", "Saved Search")
save_path = os.path.join(workflow_dir, "searches.json")

# Load existing saved searches
if os.path.exists(save_path):
    try:
        with open(save_path, "r") as f:
            saved = json.load(f)
            if not isinstance(saved, list):
                saved = []
    except:
        saved = []
else:
    saved = []

# Check for exact match
existing_queries = [s["query"] for s in saved]
if query in existing_queries:
    subprocess.run([
        "osascript", "-e",
        f'display notification "Already saved: {query}" with title "{workflow_name}"'
    ])
    sys.exit(0)

# Save to top of list
saved.insert(0, { "query": query })

# Write back (limit to 10)
with open(save_path, "w") as f:
    max_count = int(os.environ["saved_search_count"])
    json.dump(saved[:max_count], f, indent=2)


# Notify on success
subprocess.run([
    "osascript", "-e",
    f'display notification "Saved: {query}" with title "{workflow_name}"'
])
