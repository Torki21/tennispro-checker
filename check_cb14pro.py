import urllib.request
import json
import os

# Shopify .js endpoint voor directe voorraadgegevens
URL = "https://www.tennispro.nl/products/elektronische-bespanmachine-cb-14-pro.js"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

stock_file = 'stock.json'
results = {}
if os.path.exists(stock_file):
    try:
        with open(stock_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except:
        results = {}

PREFIX = "bespanmachine_cb14_pro"

try:
    req = urllib.request.Request(URL, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        is_available = data.get('available', False)
        variants = data.get('variants', [])
        
        total_qty = None
        if variants and 'inventory_quantity' in variants[0]:
            total_qty = sum(v.get('inventory_quantity', 0) for v in variants if v.get('available'))

        if not is_available:
            results[PREFIX] = {"status": "red", "text": "Niet op voorraad"}
        elif total_qty is not None and 1 <= total_qty <= 3:
            results[PREFIX] = {"status": "orange", "text": f"Nog {total_qty} op voorraad"}
        else:
            results[PREFIX] = {"status": "green", "text": "Op voorraad"}

except Exception as e:
    print(f"Fout bij {PREFIX}: {e}")

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
