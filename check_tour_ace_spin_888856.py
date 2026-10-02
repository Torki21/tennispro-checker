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

# Statussen instellen voor artikel 888856
results["tour_ace_spin_888856_120"] = {"status": "red", "text": "Niet op voorraad"}
results["tour_ace_spin_888856_125"] = {"status": "green", "text": "Op voorraad"}
results["tour_ace_spin_888856_130"] = {"status": "green", "text": "Op voorraad"}

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
