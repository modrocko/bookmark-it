import os
import urllib.parse

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
