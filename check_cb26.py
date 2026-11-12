import urllib.request
import re
import json
import os

HTML_URL = "https://www.tennispro.nl/products/elektronische-snaarbespanmachine-cb-26-zonder-standaard"
JS_URL = HTML_URL + ".js"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

stock_file = 'stock.json'
results = {}
if os.path.exists(stock_file):
    try:
        with open(stock_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except:
        results = {}

PREFIX = "cb26"

try:
    # 1. Check eerst de officiële Shopify beschikbaarheid via .js
    req_js = urllib.request.Request(JS_URL, headers=headers)
    with urllib.request.urlopen(req_js) as response:
        data = json.loads(response.read().decode('utf-8'))
        is_available = data.get('available', False)

    if not is_available:
        results[PREFIX] = {"status": "red", "text": "Niet op voorraad"}
    else:
        # 2. Haal de gewone HTML-pagina op om het exacte aantal (1-3) te vinden
        req_html = urllib.request.Request(HTML_URL, headers=headers)
        with urllib.request.urlopen(req_html) as response:
            html = response.read().decode('utf-8')
            clean_text = re.sub(r'<[^>]+>', ' ', html).replace('&nbsp;', ' ')

            match_qty = re.search(r'(?:Available\s*stock|Stock|Voorraad)\s*:?\s*(\d+)', clean_text, re.IGNORECASE)
            if not match_qty:
                match_qty = re.search(r'"inventory_quantity"\s*:\s*(\d+)', html)

            if match_qty:
                count = int(match_qty.group(1))
                if count == 0:
                    results[PREFIX] = {"status": "red", "text": "Niet op voorraad"}
                elif 1 <= count <= 3:
                    results[PREFIX] = {"status": "orange", "text": f"Nog {count} op voorraad"}
                else:
                    results[PREFIX] = {"status": "green", "text": "Op voorraad"}
            else:
                results[PREFIX] = {"status": "green", "text": "Op voorraad"}

except Exception as e:
    print(f"Fout bij {PREFIX}: {e}")

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
