import json
import os

stock_file = 'stock.json'
results = {}

# Bestaande voorraad inlezen zodat we niets overschrijven
if os.path.exists(stock_file):
    try:
        with open(stock_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except:
        results = {}

# Statussen instellen voor Tennispro Comfort Elite (888824)
results["comfort_elite_125"] = {"status": "green", "text": "Op voorraad"}
results["comfort_elite_130"] = {"status": "green", "text": "Op voorraad"}

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
