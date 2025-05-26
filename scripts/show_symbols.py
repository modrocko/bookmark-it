import json
import utils

items = []
for symbol, emoji in utils.symbol_map.items():
    items.append({
        "title": f"Type '{symbol}' for {emoji}",
        "valid": False,
        "icon": { "path": "info.png" }
    })

print(json.dumps({ "items": items }))
