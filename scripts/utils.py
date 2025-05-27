import os
import urllib.parse
import json

########################################
#get the right icon based on the current browser setting
def get_bookmark_icon():
    browser = os.environ.get("browser", "Safari")
    paths = {
        "Safari": "/System/Applications/Safari.app",
        "Google Chrome": "/Applications/Google Chrome.app",
        "Brave Browser": "/Applications/Brave Browser.app",
        "Microsoft Edge": "/Applications/Microsoft Edge.app",
        "Arc": "/Applications/Arc.app"
    }

    icon_path = paths.get(browser)
    icon = { "path": icon_path }
    if icon_path.endswith(".app"):
        icon["type"] = "fileicon"
    return icon



#########################################
#get any domain icons for a url
_icon_cache = None

def get_icon(entry, fallback_icon):
    global _icon_cache

    # Use explicit icon if set
    icon_path = entry.get("icon")
    if isinstance(icon_path, str):
        return { "path": icon_path }

    # Parse domain from URL
    url = entry.get("url", "")
    full_domain = urllib.parse.urlparse(url).netloc.split(":")[0].lower()
    domain_parts = full_domain.split(".")
    domain = domain_parts[-2] if len(domain_parts) >= 2 else full_domain
    domain_icon_file = f"{domain}.png"

    # Cache icon file names once
    if _icon_cache is None:
        workflow_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_dir = os.path.join(workflow_dir, "icons")
        _icon_cache = set(os.listdir(icon_dir)) if os.path.exists(icon_dir) else set()

    # Match icon if it exists
    if domain_icon_file in _icon_cache:
        return { "path": f"icons/{domain_icon_file}" }

    # Fallback icon
    return fallback_icon



###################################
#add items to the recent list/file
def add_to_recent(entry, tag):

    entry = dict(entry)  # make a copy
    entry["tag"] = tag

    recent_path = os.path.join(os.environ["alfred_workflow_data"], "recent.json")

    try:
        with open(recent_path) as f:
            recent = json.load(f)
    except FileNotFoundError:
        recent = []

    # remove duplicate if exists
    recent = [r for r in recent if r.get("uid") != entry.get("uid")]

    # insert to top
    recent.insert(0, entry)

    cap = int(os.environ.get("recent"))
    recent = recent[:cap]

    with open(recent_path, "w") as f:
        json.dump(recent, f, indent=2)




#######################################
# get files for an item
def get_item_fields(item, tag, bookmark_icon):
    item_type = item.get("type")
    uid = item.get("uid")
    title = ""
    subtitle = ""
    path = ""
    icon = {}

    if item_type == "file":
        path = item.get("path", "")
        title = item.get("name") or os.path.basename(path.rstrip("/"))
        subtitle = path
        icon = { "path": path, "type": "fileicon" }

    elif item_type == "email":
        title = item.get("subject", "")
        sender = item.get("sender", "")
        date = item.get("date", "")
        subtitle = f"{sender} • {date}"
        message_id = item.get("id", "")
        path = "message://" + urllib.parse.quote(f"<{message_id}>")
        icon = { "path": "/System/Applications/Mail.app", "type": "fileicon" }

    elif item_type == "bookmark":
        title = item.get("title") or item.get("url", "")
        url = item.get("url", "")
        subtitle = url
        path = url
        icon = get_icon(item, bookmark_icon)

    else:
        return None  # skip unknown

    return {
        "item_type": item_type,
        "uid": uid,
        "title": title,
        "subtitle": subtitle,
        "path": path,
        "icon": icon
    }




####################################
# load symbol map from Alfred workflow variable
raw = os.environ.get("symbols", "{}")
symbol_map_raw = json.loads(raw)

# Extract just the emoji part
symbol_map = {k: v.split(":", 1)[0].strip() for k, v in symbol_map_raw.items()}

def normalize_symbols(text):
    for k, emoji in symbol_map.items():
        text = text.replace(k, emoji)
    return text
