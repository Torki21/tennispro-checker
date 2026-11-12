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
        # 2. Haal de HTML-pagina op en zoek naar de exacte tekst ("Nog maar 2 op voorraad!")
        req_html = urllib.request.Request(HTML_URL, headers=headers)
        with urllib.request.urlopen(req_html) as response:
            html = response.read().decode('utf-8')
            clean_text = re.sub(r'<[^>]+>', ' ', html).replace('&nbsp;', ' ')
            clean_text = re.sub(r'\s+', ' ', clean_text)

            patterns_text = [
                r'(?:Nog\s*(?:maar)?|Slechts|Laatste|Only)\s*(\d+)\s*(?:op\s*voorraad|stuks|in\s*stock|left)',
                r'(?:Available\s*stock|Stock|Voorraad)\s*:?\s*(\d+)',
                r'(\d+)\s*(?:op\s*voorraad|in\s*stock|disponibles?)'
            ]
            
            count = None
            for pat in patterns_text:
                m = re.search(pat, clean_text, re.IGNORECASE)
                if m:
                    count = int(m.group(1))
                    break

            if count is None:
                patterns_html = [
                    r'"inventory_quantity"\s*:\s*(\d+)',
                    r'"inventoryQuantity"\s*:\s*(\d+)',
                    r'"quantity"\s*:\s*(\d+)',
                    r'data-inventory(?:-[a-z]+)?=["\'](\d+)["\']'
                ]
                for pat in patterns_html:
                    m = re.search(pat, html, re.IGNORECASE)
                    if m:
                        count = int(m.group(1))
                        break

            if count is not None:
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
