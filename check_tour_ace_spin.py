import json
import os

stock_file = 'stock.json'
results = {}

# Bestaande stock.json inlezen zodat we andere producten niet overschrijven
if os.path.exists(stock_file):
    try:
        with open(stock_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except:
        results = {}

# Voorraadstatussen instellen voor Tour Ace Spin
results["tour_ace_spin_120"] = {"status": "red", "text": "Niet op voorraad"}
results["tour_ace_spin_125"] = {"status": "green", "text": "Op voorraad"}
results["tour_ace_spin_130"] = {"status": "green", "text": "Op voorraad"}

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
