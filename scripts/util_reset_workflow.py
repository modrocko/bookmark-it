import os

workflow_dir = os.environ["alfred_workflow_data"]
items_path = os.path.join(workflow_dir, "items.json")

# Delete items.json if it exists
if os.path.exists(items_path):
    os.remove(items_path)

# Re-initialize the workflow
init_script_path = os.path.join(os.path.dirname(__file__), "util_init_workflow.py")
os.system(f'python3 "{init_script_path}"')