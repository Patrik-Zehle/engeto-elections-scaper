"""
main.py: Třetí projekt do Engeto Online Python Akademie (Elections Scraper)
author: Tvoje Jméno
email: tvuj.email@example.com
discord: tvojejmeno#1234
"""

import sys
import csv
import requests
from bs4 import BeautifulSoup
from typing import List, Dict


def over_argumenty() -> tuple[str, str]:
    """Zkontroluje a vrátí argumenty z příkazové řádky."""
    if len(sys.argv) != 3:
        print("Chyba: Program vyžaduje 2 argumenty: <URL> <vystup.csv>")
        sys.exit(1)
    
    url, nazev = sys.argv[1], sys.argv[2]
    if not url.startswith("https://www.volby.cz"):
        print("Chyba: URL musí být z domény volby.cz")
        sys.exit(1)
    if not nazev.endswith(".csv"):
        print("Chyba: Soubor musí mít příponu .csv")
        sys.exit(1)
    return url, nazev


def ziskej_soup(url: str) -> BeautifulSoup:
    """Stáhne stránku a vrátí BeautifulSoup objekt."""
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Chyba připojení: {e}")
        sys.exit(1)


def ziskej_seznam_obci(url: str) -> List[Dict]:
    """Vrátí seznam obcí (kód, název, url detailu)."""
    soup = ziskej_soup(url)
    obce = []
    base = url.rsplit('/', 1)[0] + '/'
    
    # Hledáme všechny tabulky s obcemi
    for t in soup.find_all("table", {"class": "table"}):
        for r in t.find_all("tr")[2:]:
            c_bunka = r.find("td", {"class": "cislo"})
            n_bunka = r.find("td", {"class": "overflow_name"})
            
            if c_bunka and n_bunka:
                link = c_bunka.find("a")
                if link:
                    obce.append({
                        "code": c_bunka.text.strip(),
                        "location": n_bunka.text.strip(),
                        "url": base + link["href"]
                    })
    return obce


def ziskej_detaily_obce(url: str) -> Dict:
    """Stáhne počty voličů a hlasy pro strany v konkrétní obci."""
    soup = ziskej_soup(url)
    data = {}
    
    # 1. Základní statistiky (Voliči, Obálky, Platné hlasy)
    # Hledáme podle hlaviček (headers) v HTML tabulce - sa2, sa3, sa6
    try:
        data["registered"] = soup.find("td", headers="sa2").text.replace('\xa0', '')
        data["envelopes"] = soup.find("td", headers="sa3").text.replace('\xa0', '')
        data["valid"] = soup.find("td", headers="sa6").text.replace('\xa0', '')
    except AttributeError:
        print(f"Chyba při parsování detailů: {url}")
    
    # 2. Hlasy pro jednotlivé strany
    # Strany jsou ve více tabulkách, projdeme je všechny
    tables = soup.find_all("table", {"class": "table"})
    for table in tables:
        for row in table.find_all("tr")[2:]:
            party = row.find("td", {"class": "overflow_name"})
            if party:
                # Hlasy jsou obvykle v následujících buňkách
                # Hledáme buňku s číslem (hlasy) - indexy se mohou lišit, hledáme tu správnou
                cols = row.find_all("td")
                # Hlasy bývají ve 2. nebo 3. sloupci s čísly
                for col in cols:
                    if col.get("headers") and ("t1sa2" in col["headers"] or "t2sa2" in col["headers"]):
                        data[party.text.strip()] = col.text.replace('\xa0', '')
                        break
    return data


def uloz_do_csv(data: List[Dict], soubor: str):
    """Uloží seznam slovníků do CSV."""
    print(f"Ukládám data do souboru: {soubor}")
    if not data:
        return

    # Získáme hlavičku ze všech klíčů prvního záznamu (včetně stran)
    fieldnames = data[0].keys()
    
    with open(soubor, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(data)


def main():
    url_okresu, soubor = over_argumenty()
    
    print(f"STAHUJI DATA Z: {url_okresu}")
    seznam_obci = ziskej_seznam_obci(url_okresu)
    print(f"Nalezeno {len(seznam_obci)} obcí. Zahajuji stahování detailů...")
    
    vysledna_data = []
    
    for i, obec in enumerate(seznam_obci, 1):
        # Výpis průběhu, aby uživatel viděl, že se něco děje
        print(f"Zpracovávám ({i}/{len(seznam_obci)}): {obec['location']}")
        
        # Stáhneme detaily (voliči, strany...)
        detaily = ziskej_detaily_obce(obec["url"])
        
        # Spojíme základní info (kód, jméno) s detaily
        komplet_obec = {**obec, **detaily}
        
        # Odstraníme URL z finálního výstupu (není v zadání CSV)
        del komplet_obec["url"]
        
        vysledna_data.append(komplet_obec)
    
    uloz_do_csv(vysledna_data, soubor)
    print("HOTOVO! 🎉")


if __name__ == "__main__":
    main()