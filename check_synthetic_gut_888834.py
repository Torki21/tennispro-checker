import urllib.request
import re
import json
import os

URL = "https://www.tennispro.nl/bobine-tennispro-synthetic-gut-200-meter-888834.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

stock_file = 'stock.json'
results = {}
if os.path.exists(stock_file):
    try:
        with open(stock_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except:
        results = {}

PREFIX = "synthetic_gut_888834"

try:
    req = urllib.request.Request(URL, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        # Algemene status
        is_out = ('"is_in_stock":false' in html.replace(" ", "") or 
                  'uit voorraad' in html.lower() or 
                  'niet op voorraad' in html.lower())
        
        results[PREFIX] = {"status": "red" if is_out else "green", "text": "Niet op voorraad" if is_out else "Op voorraad"}

        # Zoek alle varianten/diktes in de pagina HTML
        matches = re.findall(r'(1\.\d{2})\s*MM', html, re.IGNORECASE)
        found_gauges = set(matches)

        for gauge in found_gauges:
            key = f"{PREFIX}_{gauge}"
            # Als de maat in de HTML staat en de pagina is in stock, markeer als groen
            results[key] = {"status": "green" if not is_out else "red", "text": "Op voorraad" if not is_out else "Niet op voorraad"}

except Exception as e:
    print(f"Fout bij {PREFIX}: {e}")

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
