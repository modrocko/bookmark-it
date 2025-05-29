import sys
import os
import json

# Get {var:symbols} from Alfred
raw = os.environ.get("symbols", "{}")
symbol_map = json.loads(raw)

items = []
for symbol, value in symbol_map.items():
    emoji, label = [part.strip() for part in value.split(":", 1)]
    items.append({
        "title": f"Type '{symbol}' → {emoji}  ({label})",
        "valid": False,
        "icon": { "path": "info.png" }
    })

print(json.dumps({ "items": items }))
