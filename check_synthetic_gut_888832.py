import urllib.request
import re
import json
import os

URL = "https://www.tennispro.nl/bobine-tennispro-synthetic-gut-200-meter-888832.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

stock_file = 'stock.json'
results = {}
if os.path.exists(stock_file):
    try:
        with open(stock_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except:
        results = {}

PREFIX = "synthetic_gut_888832"

try:
    req = urllib.request.Request(URL, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        # Zoek alle diktematen in de HTML (bijv. 1.25MM, 1.30MM met Stock status)
        matches = re.findall(r'(1\.\d{2})\s*MM.*?Stock\s*([^<]+)', html, re.DOTALL | re.IGNORECASE)
        
        found_variants = False

        if matches:
            for gauge, stock_str in matches:
                found_variants = True
                key = f"{PREFIX}_{gauge}"
                
                if "uitverkocht" in stock_str.lower() or "0" in stock_str:
                    results[key] = {"status": "red", "text": "Niet op voorraad"}
                elif any(c in stock_str for c in ["1", "2", "3"]):
                    results[key] = {"status": "orange", "text": "Nog beperkt op voorraad"}
                else:
                    results[key] = {"status": "green", "text": "Op voorraad"}

        # Fallback indien geen losse maten worden gevonden
        if not found_variants:
            is_out = ('"is_in_stock":false' in html.replace(" ", "") or 
                      'uit voorraad' in html.lower() or 
                      'niet op voorraad' in html.lower())
            if is_out:
                results[PREFIX] = {"status": "red", "text": "Niet op voorraad"}
            else:
                results[PREFIX] = {"status": "green", "text": "Op voorraad"}

except Exception as e:
    print(f"Fout bij {PREFIX}: {e}")

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
