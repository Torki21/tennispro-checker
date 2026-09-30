import urllib.request
import re
import json

# Producten die gecontroleerd moeten worden
PRODUCTS = {
    "cb26": "https://www.tennispro.nl/cb-26-elektronische-bespanmachine-zonder-standaard-841168.html"
    "slinger_toernooipakket": "https://www.tennispro.nl/slinger-tennis-toernooipakket-841876.html"
}

results = {}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for product_id, url in PRODUCTS.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # Zoek naar qty-dispo
            match = re.search(r'class=["\'][^"\']*qty-dispo[^"\']*["\'][^>]*>([^<]+)<', html, re.IGNORECASE)
            
            if match:
                val = match.group(1).strip()
                if "+" in val:
                    results[product_id] = {"status": "green", "text": "Op voorraad", "count": val}
                else:
                    try:
                        num = int(val)
                        if num >= 3:
                            results[product_id] = {"status": "green", "text": "Op voorraad", "count": str(num)}
                        elif num >= 1:
                            results[product_id] = {"status": "orange", "text": "Beperkt beschikbaar", "count": str(num)}
                        else:
                            results[product_id] = {"status": "red", "text": "Niet op voorraad", "count": "0"}
                    except ValueError:
                        results[product_id] = {"status": "grey", "text": "Beschikbaarheid controleren", "count": "?"}
            else:
                if re.search(r'niet voorradig|rupture|indisponible', html, re.IGNORECASE):
                    results[product_id] = {"status": "red", "text": "Niet op voorraad", "count": "0"}
                else:
                    results[product_id] = {"status": "grey", "text": "Beschikbaarheid controleren", "count": "?"}

    except Exception as e:
        results[product_id] = {"status": "grey", "text": "Fout bij ophalen", "count": "?"}

# Sla op in stock.json
with open('stock.json', 'w') as f:
    json.dump(results, f, indent=2)

print("Check voltooid:", results)
