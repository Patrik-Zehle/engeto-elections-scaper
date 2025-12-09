# Elections Scraper

Tento projekt slouží ke stahování výsledků voleb do Poslanecké sněmovny Parlamentu České republiky z roku 2017. Skript stahuje data z webu [volby.cz](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) pro vybraný územní celek a ukládá je do CSV souboru.

Projekt je vypracován jako **třetí projekt do Engeto Online Python Akademie**.

## Instalace knihoven

Kód využívá knihovny třetích stran, které nejsou součástí standardní instalace Pythonu. Tyto knihovny jsou uvedeny v souboru `requirements.txt`.

Doporučuji vytvořit nové virtuální prostředí a nainstalovat knihovny následovně:

```bash
# 1. Vytvoření virtuálního prostředí
python3 -m venv venv

# 2. Aktivace virtuálního prostředí (macOS/Linux)
source venv/bin/activate
# (Windows: venv\Scripts\activate)

# 3. Instalace knihoven ze souboru
pip install -r requirements.txt


Spuštění projektu
Spuštění souboru main.py v rámci příkazové řádky vyžaduje dva povinné argumenty:

Odkaz (URL) na územní celek, který chcete stahovat (např. okres Prostějov).

Název výstupního souboru s příponou .csv.

Příklad spuštění:
python main.py "[https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103)" "vysledky_prostejov.csv"




Průběh stahování:
Program po spuštění vypíše informaci o stahování a průběžně informuje o zpracování jednotlivých obcí:
STAHUJI DATA Z: [https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103)
Nalezeno 97 obcí. Zahajuji stahování detailů...
Zpracovávám (1/97): Alojzov
Zpracovávám (2/97): Bedihošť
...
HOTOVO! 🎉
Ukládám data do souboru: vysledky_prostejov.csv




Ukázka výstupu
Výsledný soubor obsahuje následující sloupce:

Kód obce

Název obce

Počet voličů

Vydané obálky

Platné hlasy

Kandidující strany (co sloupec, to strana)

Příklad dat v CSV souboru:
code;location;registered;envelopes;valid;Občanská demokratická strana;Řád národa - Vlastenecká unie;...
506761;Alojzov;205;145;144;29;0;...
589268;Bedihošť;834;527;524;51;0;...

