import json
import os
import subprocess

workflow_data = os.getenv('alfred_workflow_data')
workflow_name = os.getenv('alfred_workflow_name', 'Tag It')

input_path = os.path.join(workflow_data, 'items.json')
output_path = os.path.join(workflow_data, 'bookmarks.md')

with open(input_path, 'r') as f:
    data = json.load(f)

with open(output_path, 'w') as f:
    for group in data:
        tag = group.get('tag', 'No tag')
        bookmarks = [
            item for item in group.get('items', [])
            if item.get('type') == 'bookmark'
        ]
        if bookmarks:
            f.write(f"## {tag}\n\n")
            for b in bookmarks:
                title = b.get('title', 'No title')
                url = b.get('url', '')
                f.write(f"- [{title}]({url})\n")
            f.write("\n")

# **Show notification**
subprocess.run([
    "osascript", "-e",
    f'display notification "Exported bookmarks to bookmarks.md" with title "{workflow_name}"'
])