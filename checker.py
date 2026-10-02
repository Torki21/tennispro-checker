import urllib.request
import re
import json

PRODUCTS = {
    "cb26": "https://www.tennispro.nl/cb-26-elektronische-bespanmachine-zonder-standaard-841168.html",
    "slinger_toernooipakket": "https://www.tennispro.nl/slinger-tennis-toernooipakket-841876.html",
    "cb14pro": "https://www.tennispro.nl/cb14pro-elektronische-bespanmachine-3760.html",
    "tour_ace_rough": "https://www.tennispro.nl/bobine-tennispro-tour-ace-rough-200-meter-888848.html"
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

            # Specifieke behandeling voor snaren met verschillende maten
            if product_id == "tour_ace_rough":
                # Standaard zetten we alle 3 de maten op "Niet op voorraad"
                sizes = {
                    "tour_ace_rough_120": {"status": "red", "text": "Niet op voorraad"},
                    "tour_ace_rough_125": {"status": "red", "text": "Niet op voorraad"},
                    "tour_ace_rough_130": {"status": "red", "text": "Niet op voorraad"}
                }
                
                # Zoek naar aanwezige maten en hun voorraadstatus in de broncode
                matches = re.findall(r'1\.([0-9]{2})\s*MM.*?Stock\s*([0-9\+]+)', html, re.IGNORECASE | re.DOTALL)
                
                if matches:
                    for gauge, stock_val in matches:
                        key = f"tour_ace_rough_1{gauge}"
                        sizes[key] = {"status": "green", "text": "Op voorraad", "count": f"Stock {stock_val}"}
                else:
                    # Alternatieve check via JSON opties in de HTML
                    options = re.findall(r'"label":\s*"([^"]+)".*?"is_in_stock":\s*(true|false)', html)
                    for label, in_stock in options:
                        clean = re.sub(r'[^0-9]', '', label)
                        if clean in ["120", "125", "130"] and in_stock == "true":
                            sizes[f"tour_ace_rough_{clean}"] = {"status": "green", "text": "Op voorraad"}

                results.update(sizes)

            else:
                # Standaard controle voor enkelvoudige producten
                match = re.search(r'class=["\'][^"\']*qty-dispo[^"\']*["\'][^>]*>([^<]+)<', html, re.IGNORECASE)
                if match:
                    val = match.group(1).strip()
                    if "+" in val or "voorraad" in val.lower():
                        results[product_id] = {"status": "green", "text": "Op voorraad", "count": val}
                    else:
                        results[product_id] = {"status": "red", "text": "Niet op voorraad", "count": val}
                else:
                    results[product_id] = {"status": "green", "text": "Op voorraad"}

    except Exception as e:
        print(f"Fout bij ophalen van {product_id}: {e}")

# Opslaan in stock.json
with open('stock.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
