import urllib.request
import re
import json
import os

URL = "https://www.tennispro.nl/bobine-tennispro-tour-ace-rough-200-meter-888848.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

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
        
        # Wij zoeken specifiek naar de opties in het keuzemenu (1.20MM, 1.25MM, 1.30MM)
        gauges = ['120', '125', '130']
        
        for g in gauges:
            key = f"tour_ace_rough_{g}"
            
            # Maak de zoekterm voor de dikte (bijv. "1.25")
            dikte_label = f"1.{g[1:]}" if len(g) == 3 else g
            
            # Zoek in de HTML naar het stukje rondom deze dikte in het keuzemenu
            # Bijv. "1.25MM" gevolgd door "Stock 5+" of "Niet op voorraad"
            pattern = re.compile(rf'{dikte_label}\s*MM.*?(Stock\s*\d+\+?|Niet op voorraad|Uit verkocht)', re.IGNORECASE | re.DOTALL)
            match = pattern.search(html)
            
            if match:
                stock_str = match.group(1).lower()
                
                if 'niet' in stock_str or 'uit' in stock_str:
                    results[key] = {"status": "red", "text": "Niet op voorraad"}
                else:
                    # Haal het getal op uit bijv. "Stock 5+" of "Stock 2"
                    numbers = re.findall(r'\d+', stock_str)
                    count = int(numbers[0]) if numbers else 5
                    
                    if count == 0:
                        results[key] = {"status": "red", "text": "Niet op voorraad"}
                    elif 1 <= count <= 3:
                        results[key] = {"status": "orange", "text": f"Nog {count} stuks op voorraad"}
                    else:
                        results[key] = {"status": "green", "text": "Op voorraad"}
            else:
                # Als de specifieke dikte (zoals 1.20MM) helemaal NIET in de keuzelijst staat, is deze uitverkocht!
                dikte_in_html = re.search(rf'{dikte_label}\s*MM', html, re.IGNORECASE)
                if not dikte_in_html:
                    results[key] = {"status": "red", "text": "Niet op voorraad"}
                else:
                    results[key] = {"status": "green", "text": "Op voorraad"}

except Exception as e:
    print(f"Fout bij Tour Ace Rough: {e}")

with open(stock_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
