#!/usr/bin/env python3
import json
import os

# Test data loading exactly like Flask app
LEGAL_DATA = {}
ANALYSIS_REPORT = {}

try:
    # Load legal data
    if os.path.exists('complete_uzbekistan_legal_codes.json'):
        with open('complete_uzbekistan_legal_codes.json', 'r', encoding='utf-8') as f:
            complete_data = json.load(f)
            LEGAL_DATA = complete_data.get('kodekslar', {})
            print(f"Legal data loaded: {len(LEGAL_DATA)} codes")
    
    # Load analysis report
    if os.path.exists('analysis_report.json'):
        with open('analysis_report.json', 'r', encoding='utf-8') as f:
            ANALYSIS_REPORT = json.load(f)
            print(f"Analysis report loaded: {bool(ANALYSIS_REPORT)}")
    
    # Check template variables
    print("\n=== TEMPLATE VARIABLES ===")
    print(f"total_codes: {ANALYSIS_REPORT.get('total_codes', 0)}")
    print(f"total_articles: {ANALYSIS_REPORT.get('total_articles', 0)}")
    print(f"average_confidence_score: {ANALYSIS_REPORT.get('average_confidence_score', 0)}")
    print(f"domain_distribution length: {len(ANALYSIS_REPORT.get('domain_distribution', {}))}")
    
    # Calculate actual values
    actual_total_codes = len(LEGAL_DATA)
    actual_total_articles = sum(len(code_data.get('moddalar', [])) for code_data in LEGAL_DATA.values())
    
    print(f"\n=== ACTUAL VALUES ===")
    print(f"Actual codes: {actual_total_codes}")
    print(f"Actual articles: {actual_total_articles}")
    
    # Check if they match
    if actual_total_codes == ANALYSIS_REPORT.get('total_codes', 0):
        print("Codes match!")
    else:
        print("Codes DON'T match!")
        
    if actual_total_articles == ANALYSIS_REPORT.get('total_articles', 0):
        print("Articles match!")
    else:
        print("Articles DON'T match!")

except Exception as e:
    print(f"Error: {e}")
