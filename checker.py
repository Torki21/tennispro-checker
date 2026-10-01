import urllib.request
import re
import json

# Producten die gecontroleerd moeten worden
PRODUCTS = {
    "cb26": "https://www.tennispro.nl/cb-26-elektronische-bespanmachine-zonder-standaard-841168.html",
    "slinger_toernooipakket": "https://www.tennispro.nl/slinger-tennis-toernooipakket-841876.html",
    "cb14pro": "https://www.tennispro.nl/cb14pro-elektronische-bespanmachine-3760.html",
    
    # Tour Ace Rough varianten (link naar de overkoepelende pagina)
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

            # Controleer of de pagina varianten/opties bevat (JSON config op Tennispro)
            config_match = re.search(r'\[data-role=swatch-options\]":\s*(\{\s*"\[data-role=swatch-option-validator\]":.*?\})\s*\}', html, re.DOTALL)
            
            if config_match:
                # Als er opties/varianten zijn (zoals snaardiktes)
                # Koppel de voorraad per optie los
                options = re.findall(r'"label":\s*"([^"]+)".*?"is_in_stock":\s*(true|false)', html)
                for label, in_stock in options:
                    clean_label = re.sub(r'[^a-zA-Z0-9]', '', label).lower()
                    var_key = f"{product_id}_{clean_label}"
                    
                    status = "green" if in_stock == "true" else "red"
                    results[var_key] = {"status": status, "text": "Op voorraad" if status == "green" else "Niet op voorraad"}
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
    json.dump(results, f, ensure_ascii=False, indent=2)import urllib.request
import re
import json

# Producten die gecontroleerd moeten worden
PRODUCTS = {
    "cb26": "https://www.tennispro.nl/cb-26-elektronische-bespanmachine-zonder-standaard-841168.html",
    "slinger_toernooipakket": "https://www.tennispro.nl/slinger-tennis-toernooipakket-841876.html",
    "cb14pro": "https://www.tennispro.nl/cb14pro-elektronische-bespanmachine-3760.html",
    
    # Tour Ace Rough varianten (link naar de overkoepelende pagina)
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

            # Controleer of de pagina varianten/opties bevat (JSON config op Tennispro)
            config_match = re.search(r'\[data-role=swatch-options\]":\s*(\{\s*"\[data-role=swatch-option-validator\]":.*?\})\s*\}', html, re.DOTALL)
            
            if config_match:
                # Als er opties/varianten zijn (zoals snaardiktes)
                # Koppel de voorraad per optie los
                options = re.findall(r'"label":\s*"([^"]+)".*?"is_in_stock":\s*(true|false)', html)
                for label, in_stock in options:
                    clean_label = re.sub(r'[^a-zA-Z0-9]', '', label).lower()
                    var_key = f"{product_id}_{clean_label}"
                    
                    status = "green" if in_stock == "true" else "red"
                    results[var_key] = {"status": status, "text": "Op voorraad" if status == "green" else "Niet op voorraad"}
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
