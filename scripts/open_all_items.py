import sys
import subprocess

tag = sys.argv[1].strip()

for item_type in ["file", "bookmark", "email"]:
    subprocess.run(["python3", "scripts/open_items.py", f"{tag}||{item_type}"])
