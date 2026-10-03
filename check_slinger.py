import urllib.request
import re
import json
import os

URL = "https://www.tennispro.nl/slinger-tennis-toernooipakket-841876.html"
headers = {'User-Agent': 'Mozilla/5.0'}

stock_file = 'stock.json'
results = {}
if os.path.exists(stock_file):
    try:
        with open(stock_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except:
        results = {}

try:
    req = urllib.request.Request(URL, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        is_out = ('"is_in_stock":false' in html.replace(" ", "") or 
                  'uit voorraad' in html.lower() or 
                  'momenteel niet beschikbaar' in html.lower())
        
        # Zoek naar aantal stuks in de HTML
        match_qty = re.search(r'class=["\'][^"\']*qty-dispo[^"\']*["\'][^>]*>([^<]+)<', html, re.IGNORECASE)
        
        if is_out:
            results["cb26"] = {"status": "red", "text": "Niet op voorraad"}
        elif match_qty:
            raw_val = match_qty.group(1).strip()
            # Haal enkel het getal op
            numbers = re.findall(r'\d+', raw_val)
            count = int(numbers[0]) if numbers else 0
            
            if count == 0:
                results["cb26"] = {"status": "red", "text": "Niet op voorraad"}
            elif 1 <= count <= 3:
                results["cb26"] = {"status": "orange", "text": f"Nog {count} op voorraad"}
            else:
                results["cb26"] = {"status": "green", "text": "Op voorraad"}
        else:
            results["cb26"] = {"status": "green", "text": "Op voorraad"}
except Exception as e:
    print(f"Fout bij CB-26: {e}")

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
