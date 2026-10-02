import urllib.request
import re
import json
import os

URL = "https://www.tennispro.nl/cb-26-elektronische-bespanmachine-zonder-standaard-841168.html"
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
        
        match_qty = re.search(r'class=["\'][^"\']*qty-dispo[^"\']*["\'][^>]*>([^<]+)<', html, re.IGNORECASE)
        
        if is_out:
            results["cb26"] = {"status": "red", "text": "Niet op voorraad"}
        elif match_qty:
            val = match_qty.group(1).strip()
            results["cb26"] = {"status": "green", "text": "Op voorraad", "count": val}
        else:
            results["cb26"] = {"status": "green", "text": "Op voorraad"}
except Exception as e:
    print(f"Fout bij CB-26: {e}")

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
