import re
import csv
import urllib.request

def main():
    print("Fetching card data from playriftbound.com...")
    url = "https://playriftbound.com/en-us/card-gallery/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch website: {e}")
        return

    print("Parsing card data...")
    # Regex to extract card JSON objects from the Next.js page data
    matches = re.finditer(r'\{"id":"([a-z]+-\d+-\d+)","collectorNumber":\d+,"name":"([^"]+)",(.*?)"cardImage":\{"type":"image","provider":"sanity","url":"([^"]+)".*?\}', html)
    
    cards = []
    for match in matches:
        card_id = match.group(1)
        name = match.group(2)
        middle_data = match.group(3)
        img_url = match.group(4).replace('\\"', '"').replace('\\\\', '\\')
        
        # Extract Set Code
        set_code = card_id.split('-')[0].upper()
        
        # Extract Type
        type_match = re.search(r'"cardType":\{.*?"type":\[\{"id":"([^"]+)"', middle_data)
        card_type = type_match.group(1).upper() if type_match else "UNKNOWN"
        
        # Extract Color(s)
        colors = []
        domain_match = re.search(r'"domain":\{.*?"values":\[(.*?)\]\}', middle_data)
        if domain_match:
            color_matches = re.finditer(r'"id":"([^"]+)"', domain_match.group(1))
            colors = [m.group(1).upper() for m in color_matches]
        color_str = "&".join(colors) if colors else "NONE"
        
        # Default Alt/Overnumbered (advanced parsing could refine this)
        altArt = 'false'
        overnumbered = 'false'
        
        cards.append({
            "name": name,
            "set": set_code,
            "quantity": 1, # default
            "type": card_type,
            "color": color_str,
            "altArt": altArt,
            "overnumbered": overnumbered,
            "image": img_url.split('?')[0] # Using direct image URL (hotlink)
        })
        
    print(f"Successfully extracted {len(cards)} cards!")
    
    output_file = "all_cards_database.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "set", "quantity", "type", "color", "altArt", "overnumbered", "image"])
        writer.writeheader()
        writer.writerows(cards)
    
    print(f"Saved complete card database to {output_file}.")

if __name__ == "__main__":
    main()
