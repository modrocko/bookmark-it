import os
import json
import subprocess

# Paths
workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")
title = os.environ["alfred_workflow_name"]

# If already setup, skip
if os.path.exists(items_path):
    subprocess.run([
        "osascript", "-e",
        f'display notification "Setup skipped — items.json already exists." with title "{title}"'
    ])
    exit(0)

# Create directory
os.makedirs(workflow_dir, exist_ok=True)

# Create items.json
with open(items_path, 'w') as f:
    json.dump([], f, indent=2)

# Notify success
subprocess.run([
    "osascript", "-e",
    f'display notification "Setup complete — items.json created." with title "{title}"'
])