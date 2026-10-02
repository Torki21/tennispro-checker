import json
import os

stock_file = 'stock.json'
results = {}
if os.path.exists(stock_file):
    try:
        with open(stock_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except:
        results = {}

results["tour_ace_rough_120"] = {"status": "red", "text": "Niet op voorraad"}
results["tour_ace_rough_125"] = {"status": "green", "text": "Op voorraad"}
results["tour_ace_rough_130"] = {"status": "green", "text": "Op voorraad"}

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
