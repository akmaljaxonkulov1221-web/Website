#!/usr/bin/env python3
import json

# Load the current data
with open('complete_uzbekistan_legal_codes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert to our system format
converted_data = {
    "kodekslar": data["legal_data"],
    "jami_kodekslar": len(data["legal_data"]),
    "jami_moddalar": sum(len(kodeks.get("moddalar", [])) for kodeks in data["legal_data"].values())
}

# Save converted data
with open('complete_uzbekistan_legal_codes.json', 'w', encoding='utf-8') as f:
    json.dump(converted_data, f, ensure_ascii=False, indent=2)

print(f"Converted {converted_data['jami_kodekslar']} codes with {converted_data['jami_moddalar']} articles")
