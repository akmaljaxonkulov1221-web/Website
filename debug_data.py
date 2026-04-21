#!/usr/bin/env python3
import json
import os

# Load the data exactly like the Flask app does
LEGAL_DATA = {}

try:
    if os.path.exists('complete_uzbekistan_legal_codes.json'):
        with open('complete_uzbekistan_legal_codes.json', 'r', encoding='utf-8') as f:
            complete_data = json.load(f)
            LEGAL_DATA = complete_data.get('kodekslar', {})
            print(f"Loaded complete legal data: {complete_data.get('jami_kodekslar')} codes with {complete_data.get('jami_moddalar')} articles")
    elif os.path.exists('professional_legal_data.json'):
        with open('professional_legal_data.json', 'r', encoding='utf-8') as f:
            LEGAL_DATA = json.load(f)
            print(f"Loaded professional legal data: {len(LEGAL_DATA)} codes")
    
    print(f"\n=== DEBUG INFO ===")
    print(f"LEGAL_DATA type: {type(LEGAL_DATA)}")
    print(f"LEGAL_DATA keys count: {len(LEGAL_DATA)}")
    print(f"LEGAL_DATA keys: {list(LEGAL_DATA.keys())}")
    
    # Check first code structure
    if LEGAL_DATA:
        first_code = list(LEGAL_DATA.keys())[0]
        first_code_data = LEGAL_DATA[first_code]
        print(f"\nFirst code: {first_code}")
        print(f"First code type: {type(first_code_data)}")
        print(f"First code keys: {list(first_code_data.keys()) if isinstance(first_code_data, dict) else 'Not a dict'}")
        
        if 'moddalar' in first_code_data:
            moddalar = first_code_data['moddalar']
            print(f"Moddalar count: {len(moddalar)}")
            print(f"First modda: {moddalar[0] if moddalar else 'No moddalar'}")
    
except Exception as e:
    print(f"Error loading data: {e}")
