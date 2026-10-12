import urllib.request
import re
import json
import os

URL = "https://www.tennispro.nl/babolat-team-all-court-karton-18-x-4-ballen-372773.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

stock_file = 'stock.json'
results = {}
if os.path.exists(stock_file):
    try:
        with open(stock_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except:
        results = {}

PREFIX = "babolat_team_372773"

try:
    req = urllib.request.Request(URL, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        is_out = ('"is_in_stock":false' in html.replace(" ", "") or 
                  'uit voorraad' in html.lower() or 
                  'momenteel niet beschikbaar' in html.lower() or
                  'niet op voorraad' in html.lower())
        
        match_qty = re.search(r'Available\s*stock\s*:\s*(\d+)', html, re.IGNORECASE)
        if not match_qty:
            match_qty = re.search(r'Stock\s*:?\s*(\d+)', html, re.IGNORECASE)

        if is_out:
            results[PREFIX] = {"status": "red", "text": "Niet op voorraad"}
        elif match_qty:
            count = int(match_qty.group(1))
            if count == 0:
                results[PREFIX] = {"status": "red", "text": "Niet op voorraad"}
            elif 1 <= count <= 3:
                results[PREFIX] = {"status": "orange", "text": f"Nog {count} dozen op voorraad"}
            else:
                results[PREFIX] = {"status": "green", "text": "Op voorraad"}
        else:
            results[PREFIX] = {"status": "green", "text": "Op voorraad"}

except Exception as e:
    print(f"Fout bij {PREFIX}: {e}")

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
