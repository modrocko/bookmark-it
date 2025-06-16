import json
import os
import subprocess

workflow_data = os.getenv('alfred_workflow_data')
workflow_name = os.getenv('alfred_workflow_name', 'Tag It')

input_path = os.path.join(workflow_data, 'items.json')
output_path = os.path.join(workflow_data, 'webpages.md')

with open(input_path, 'r') as f:
    data = json.load(f)

with open(output_path, 'w') as f:
    for group in data:
        tag = group.get('tag', 'No tag')
        webpages = [
            item for item in group.get('items', [])
            if item.get('type') == 'webpage'
        ]
        if webpages:
            f.write(f"## {tag}\n\n")
            for b in webpages:
                title = b.get('title', 'No title')
                url = b.get('url', '')
                f.write(f"- [{title}]({url})\n")
            f.write("\n")

# **Show notification**
subprocess.run([
    "osascript", "-e",
    f'display notification "Exported webpages to webpages.md" with title "{workflow_name}"'
])