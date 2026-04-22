#!/usr/bin/env python3
import json

# Load the data with UTF-8 encoding
with open('complete_uzbekistan_legal_codes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== KODEKSLAR HOLATI ===")
print(f"Jami kodekslar soni: {len(data['kodekslar'])}")
print(f"Jami moddalar soni: {data['jami_moddalar']}")
print()

print("Kodekslar ro'yxati:")
for i, (kodeks_name, kodeks_data) in enumerate(data['kodekslar'].items(), 1):
    moddalar_soni = len(kodeks_data.get('moddalar', []))
    print(f"{i}. {kodeks_name} - {moddalar_soni} ta modda")

print()
print("Birinchi kodeksning birinchi moddasi:")
first_kodeks = list(data['kodekslar'].keys())[0]
first_modda = data['kodekslar'][first_kodeks]['moddalar'][0]
print(f"Kodeks: {first_modda['kodeks']}")
print(f"Modda: {first_modda['modda']}")
print(f"Nomi: {first_modda['nomi'][:100]}...")
