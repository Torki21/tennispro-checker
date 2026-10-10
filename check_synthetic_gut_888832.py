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
        
        # Controleer globale uitverkocht-status
        is_out = ('"is_in_stock":false' in html.replace(" ", "") or 
                  'uit voorraad' in html.lower() or 
                  'momenteel niet beschikbaar' in html.lower() or
                  'niet op voorraad' in html.lower())

        # Zoek eventuele diktes/varianten in de opties
        options = re.findall(r'<option[^>]*>([^<]+)</option>', html)
        found_variants = False

        for opt in options:
            opt_clean = opt.strip()
            # Zoek naar diktematen zoals 1.25, 1.30, 1.35
            match_gauge = re.search(r'(1\.\d{2})', opt_clean)
            if match_gauge:
                found_variants = True
                gauge = match_gauge.group(1)
                key = f"{PREFIX}_{gauge}"

                if "uitverkocht" in opt_clean.lower() or "niet op voorraad" in opt_clean.lower():
                    results[key] = {"status": "red", "text": "Niet op voorraad"}
                else:
                    results[key] = {"status": "green", "text": "Op voorraad"}

        # Indien het product geen losse keuzemenu-opties heeft
        if not found_variants:
            if is_out:
                results[PREFIX] = {"status": "red", "text": "Niet op voorraad"}
            else:
                results[PREFIX] = {"status": "green", "text": "Op voorraad"}

except Exception as e:
    print(f"Fout bij {PREFIX}: {e}")

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
