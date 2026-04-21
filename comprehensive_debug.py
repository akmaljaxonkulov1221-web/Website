#!/usr/bin/env python3
import json
import os

# Simulate exact Flask app behavior
LEGAL_DATA = {}
ANALYSIS_REPORT = {}

def load_data():
    """Ma'lumotlarni yuklash - Flask app copy"""
    global LEGAL_DATA, ANALYSIS_REPORT
    
    try:
        # To'liq legal codes ma'lumotlarini yuklash
        if os.path.exists('complete_uzbekistan_legal_codes.json'):
            with open('complete_uzbekistan_legal_codes.json', 'r', encoding='utf-8') as f:
                complete_data = json.load(f)
                LEGAL_DATA = complete_data.get('kodekslar', {})
                print(f"Loaded complete legal data: {complete_data.get('jami_kodekslar')} codes with {complete_data.get('jami_moddalar')} articles")
        elif os.path.exists('professional_legal_data.json'):
            with open('professional_legal_data.json', 'r', encoding='utf-8') as f:
                LEGAL_DATA = json.load(f)
                print(f"Loaded professional legal data: {len(LEGAL_DATA)} codes")
        
        # Hisobotni yuklash
        if os.path.exists('analysis_report.json'):
            with open('analysis_report.json', 'r', encoding='utf-8') as f:
                ANALYSIS_REPORT = json.load(f)
                print("Loaded analysis report")
                
    except Exception as e:
        print(f"Error loading data: {e}")

# Load data
load_data()

# Check exact template variables
print("\n=== EXACT TEMPLATE VARIABLES ===")
print(f"analysis_report type: {type(ANALYSIS_REPORT)}")
print(f"analysis_report keys: {list(ANALYSIS_REPORT.keys()) if ANALYSIS_REPORT else 'Empty'}")

# Simulate template rendering
template_vars = {
    'legal_codes': list(LEGAL_DATA.keys()),
    'analysis_report': ANALYSIS_REPORT
}

print(f"\nlegal_codes count: {len(template_vars['legal_codes'])}")
print(f"legal_codes: {template_vars['legal_codes']}")

# Check specific template expressions
print(f"\n=== TEMPLATE EXPRESSIONS ===")
print(f"analysis_report.total_codes: {template_vars['analysis_report'].get('total_codes', 0)}")
print(f"analysis_report.total_articles: {template_vars['analysis_report'].get('total_articles', 0)}")
print(f"analysis_report.average_confidence_score: {template_vars['analysis_report'].get('average_confidence_score', 0)}")
print(f"analysis_report.domain_distribution|length: {len(template_vars['analysis_report'].get('domain_distribution', {}))}")

# Print full analysis report
print(f"\n=== FULL ANALYSIS REPORT ===")
print(json.dumps(ANALYSIS_REPORT, indent=2, ensure_ascii=False))
