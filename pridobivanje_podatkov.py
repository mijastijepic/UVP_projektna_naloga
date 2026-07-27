import re
import time
 
import requests
from bs4 import BeautifulSoup
 
import konstante as KONST


# -------------------------------------------------------------------
# POMOŽNA FUNKCIJA: prenese stran in jo pretvori v BeautifulSoup objekt
# -------------------------------------------------------------------

def pridobi_soup(url):

    # Obišče podano spletno stran in vrne njeno vsebino kot BeautifulSoup objekt, po katerem lahko nato iščemo podatke.

    try:
        odgovor = requests.get(url, headers=KONST.GLAVE, timeout=10)
        odgovor.raise_for_status()  # sproži napako, če stran ni bila najdena (npr. 404)

    except requests.RequestException as napaka:
        print(f"Napaka pri nalaganju strani {url}: {napaka}")
        return None
 
    return BeautifulSoup(odgovor.text, "html.parser")



# -------------------------------------------------------------------
# funkcija, ki pridobi seznam igralcev za eno ekipo
# -------------------------------------------------------------------

def pridobi_seznam_igralcev(spol, id_ekipe):

    url = KONST.URL_IGRALCI_EKIPE.format(spol=spol, id_ekipe=id_ekipe)
    
    soup = pridobi_soup(url)
    if soup is None:
        return []
 
    igralci = []
 
    for vrstica in soup.find_all("tr"):
        celice = vrstica.find_all("td")
        if len(celice) != 3:
            continue  # to ni vrstica z igralcem (npr. glava tabele)
 
        celica_imena = celice[1]
        povezava = celica_imena.find("a")
        if povezava is None or not povezava.get("href"):
            continue  # npr. trener nima povezave na svojo stran, zato ga preskočimo
 
        ujemanje = re.search(r"(\d+)/?$", povezava["href"])
        if ujemanje is None:
            continue
 
        igralci.append({
            "id_igralca": ujemanje.group(1),
            "st_dresa": celice[0].get_text(strip=True),
            "ime_na_seznamu": celica_imena.get_text(strip=True),
            "pozicija_kratica": celice[2].get_text(strip=True),
        })
        
 
    return igralci