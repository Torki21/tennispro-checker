import urllib.request
import re
import json

PRODUCTS = {
    "cb26": "https://www.tennispro.nl/cb-26-elektronische-bespanmachine-zonder-standaard-841168.html",
    "slinger_toernooipakket": "https://www.tennispro.nl/slinger-tennis-toernooipakket-841876.html",
    "cb14pro": "https://www.tennispro.nl/cb14pro-elektronische-bespanmachine-3760.html",
    "tour_ace_rough": "https://www.tennispro.nl/bobine-tennispro-tour-ace-rough-200-meter-888848.html",
    "tour_ace_spin": "https://www.tennispro.nl/tennispro-tour-ace-spin-spoel-200-meter-888852.html"
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

            # Specifieke behandeling voor snaren met maten (Tour Ace Rough & Tour Ace Spin)
            if product_id in ["tour_ace_rough", "tour_ace_spin"]:
                sizes = {
                    f"{product_id}_120": {"status": "red", "text": "Niet op voorraad"},
                    f"{product_id}_125": {"status": "red", "text": "Niet op voorraad"},
                    f"{product_id}_130": {"status": "red", "text": "Niet op voorraad"}
                }
                
                for gauge in ["120", "125", "130"]:
                    gauge_formatted = gauge[0] + r'[\.,]' + gauge[1:]
                    pattern = rf'"{gauge_formatted}[^"]*".*?("is_in_stock"|"is_salable"|"qty")\s*:\s*(true|false|[0-9]+)'
                    match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
                    
                    if match:
                        val = match.group(2).lower()
                        if val == "true" or (val.isdigit() and int(val) > 0):
                            sizes[f"{product_id}_{gauge}"] = {"status": "green", "text": "Op voorraad"}
                        else:
                            sizes[f"{product_id}_{gauge}"] = {"status": "red", "text": "Niet op voorraad"}
                    else:
                        # Controle via algemene voorraadmelding op pagina
                        if "in voorraad" in html.lower() or "op voorraad" in html.lower() or "qty-dispo" in html.lower():
                            # Als specifieke optie niet gevonden is maar pagina geeft in voorraad aan
                            sizes[f"{product_id}_{gauge}"] = {"status": "green", "text": "Op voorraad"}

                results.update(sizes)

            else:
                # Gewone producten
                is_out_of_stock = (
                    '"is_in_stock":false' in html.replace(" ", "") or 
                    'class="out-of-stock"' in html.lower() or
                    'uit voorraad' in html.lower() or
                    'momenteel niet beschikbaar' in html.lower()
                )
                
                match_qty = re.search(r'class=["\'][^"\']*qty-dispo[^"\']*["\'][^>]*>([^<]+)<', html, re.IGNORECASE)
                
                if is_out_of_stock:
                    results[product_id] = {"status": "red", "text": "Niet op voorraad"}
                elif match_qty:
                    val = match_qty.group(1).strip()
                    if "0" in val and "+" not in val:
                        results[product_id] = {"status": "red", "text": "Niet op voorraad", "count": val}
                    else:
                        results[product_id] = {"status": "green", "text": "Op voorraad", "count": val}
                else:
                    results[product_id] = {"status": "green", "text": "Op voorraad"}

    except Exception as e:
        print(f"Fout bij ophalen van {product_id}: {e}")

# Opslaan in stock.json
with open('stock.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
