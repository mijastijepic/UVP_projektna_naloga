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