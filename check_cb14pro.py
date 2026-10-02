import urllib.request
import json
import os

URL = "https://www.tennispro.nl/cb14pro-elektronische-bespanmachine-3760.html"
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
        is_out = ('"is_in_stock":false' in html.replace(" ", "") or 'uit voorraad' in html.lower())
        results["cb14pro"] = {"status": "red" if is_out else "green", "text": "Niet op voorraad" if is_out else "Op voorraad"}
except Exception as e:
    print(f"Fout bij CB14Pro: {e}")

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
