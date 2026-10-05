import urllib.request
import re
import json
import os

URL = "https://www.tennispro.nl/tennispro-comfort-elite-haspel-200-meter-888822.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

stock_file = 'stock.json'
results = {}
if os.path.exists(stock_file):
    try:
        with open(stock_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except:
        results = {}

PREFIX = "comfort_elite_888822"
ALL_GAUGES = ['120', '125', '130']

try:
    req = urllib.request.Request(URL, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        # Zoek dynamisch alle opties uit de dropdown HTML (e.g. "1.25MM Stock 5+")
        options = re.findall(r'(\d[.,]\d{2})\s*MM.*?(Stock\s*\d+\+?|Niet op voorraad|Uit verkocht)?', html, re.IGNORECASE)
        
        found_gauges = set()
        
        for dikte_raw, status_raw in options:
            g_key = dikte_raw.replace('.', '').replace(',', '')
            key = f"{PREFIX}_{g_key}"
            found_gauges.add(g_key)
            
            status_clean = status_raw.lower() if status_raw else ''
            
            if 'niet' in status_clean or 'uit' in status_clean:
                results[key] = {"status": "red", "text": "Niet op voorraad"}
            elif 'stock' in status_clean:
                numbers = re.findall(r'\d+', status_clean)
                count = int(numbers[0]) if numbers else 5
                
                if count == 0:
                    results[key] = {"status": "red", "text": "Niet op voorraad"}
                elif 1 <= count <= 3:
                    results[key] = {"status": "orange", "text": f"Nog {count} stuks op voorraad"}
                else:
                    results[key] = {"status": "green", "text": "Op voorraad"}
            else:
                results[key] = {"status": "green", "text": "Op voorraad"}

        # Zet eventuele verdwenen diktes automatisch op rood
        for g in ALL_GAUGES:
            if g not in found_gauges:
                results[f"{PREFIX}_{g}"] = {"status": "red", "text": "Niet op voorraad"}

except Exception as e:
    print(f"Fout bij {PREFIX}: {e}")

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
