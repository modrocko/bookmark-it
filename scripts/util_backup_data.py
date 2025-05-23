import os
import shutil
import time
import subprocess

# Setup paths
workflow_data = os.environ['alfred_workflow_data']
source_file = os.path.join(workflow_data, 'items.json')
backup_dir = os.path.join(workflow_data, 'backups')
workflow_name = os.getenv('alfred_workflow_name', 'Tag It')

# Make sure backup folder exists
os.makedirs(backup_dir, exist_ok=True)

# Only back up if items.json exists
if os.path.exists(source_file):
    timestamp = time.strftime("%Y-%m-%d-%H%M")
    backup_file = os.path.join(backup_dir, f"items {timestamp}.json")
    shutil.copy2(source_file, backup_file)

    # Keep only latest 10 backups
    backups = sorted(
        [f for f in os.listdir(backup_dir) if f.startswith("items") and f.endswith(".json")]
    )
    while len(backups) > 10:
        old = backups.pop(0)
        os.remove(os.path.join(backup_dir, old))

# **Show notification**
subprocess.run([
    "osascript", "-e",
    f'display notification "Exported all items to /backup folder" with title "{workflow_name}"'
])