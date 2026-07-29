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
 
    return BeautifulSoup(odgovor.text, "html5lib")



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
            continue  # npr. trener - nima povezave na svojo stran, zato ga preskočimo
 
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




# -------------------------------------------------------------------
# funkcija, ki zbere osebne podatke igralca
# -------------------------------------------------------------------

def ujemanje_oznake(besedilo, iskana_oznaka):

    if besedilo is None:
        return False
    return besedilo.strip() == iskana_oznaka



def vrednost_za_bio_oznako(soup, oznaka):

    def preveri_element(besedilo):
        return ujemanje_oznake(besedilo, oznaka)

    oznaka_div = soup.find(
        "div",
        class_="vbw-player-bio-head",
        string=preveri_element, # najde element kjer funkcija preveri_element vrne true
    )

    if oznaka_div is None:
        return None
 
    stolpec = oznaka_div.find_parent("div", class_="vbw-player-bio-col")
    if stolpec is None:
        return None
 
    vrednosti = stolpec.find_all("div", class_="vbw-player-bio-text")
    if not vrednosti:
        return None
 
    for vrednost in vrednosti:
        if "--desktop" in vrednost.get("class", []):
            return vrednost.get_text(strip=True)

    return vrednosti[0].get_text(strip=True)



def pridobi_bio_igralca(soup):
    return {
        "pozicija": vrednost_za_bio_oznako(soup, "Position"),
        "drzava": vrednost_za_bio_oznako(soup, "Nationality"),
        "starost": vrednost_za_bio_oznako(soup, "Age"),
        "datum_rojstva": vrednost_za_bio_oznako(soup, "Birth date"),
        "visina_cm": vrednost_za_bio_oznako(soup, "Height"),
    }



# -------------------------------------------------------------------
# funkcija, ki pridobi igralčevo statistiko
# -------------------------------------------------------------------

IMENA_STATISTIK = [
    "tocke_skupaj",           # Total Points
    "tocke_povprecje",        # Average by Match
    "tocke_napad",            # Attack Points
    "ucinkovitost_napad",     # Efficiency (%)
    "napad_povprecje",        # Avg Points (pri napadu)
    "tocke_blok",             # Block Points
    "uspesnost_blok",         # Success (%)
    "blok_povprecje",         # Avg Points (pri bloku)
    "tocke_servis",           # Serve Points
    "uspesnost_servis",       # Success (%)
    "servis_povprecje",       # Avg Points (pri servisu)
]

# Pri povprečjih (Avg Points) je mišljeno povprečno število točk na tekmo.


def preveri_zacetek_statistike(besedilo):
    return ujemanje_oznake(besedilo, "Player Competition Statistics")
 
 
def pridobi_statistiko_igralca(soup):
    
    # Iz strani igralca prebere statistiko iz razdelka "Player Competition Statistics".

    zacetna_oznaka = soup.find(string=preveri_zacetek_statistike)
    if zacetna_oznaka is None:
        return {ime: None for ime in IMENA_STATISTIK}
 
    stevilo_potrebnih_nizov = len(IMENA_STATISTIK) * 2
    nizi = []
    trenutni_element = zacetna_oznaka
 
    while len(nizi) < stevilo_potrebnih_nizov:
        trenutni_element = trenutni_element.find_next(string=True)

        if trenutni_element is None:
            break
        
        besedilo = trenutni_element.strip()

        if not besedilo:  # preskočimo prazne nize (presledki, prelomi vrstic), ki so v pythonu obravnavani kot False
            continue

        if besedilo == "%" and nizi:
            nizi[-1] += besedilo
        else:
            nizi.append(besedilo)
 
    vrednosti = nizi[1::2]
 
    statistika = {}
    for ime_polja, vrednost in zip(IMENA_STATISTIK, vrednosti):
        statistika[ime_polja] = vrednost
 
    return statistika



# -------------------------------------------------------------------
# funkcija, ki pridobi vse podatke enega igralca (bio + statistika skupaj)
# -------------------------------------------------------------------

def pridobi_podatke_igralca(id_igralca):

    url = KONST.URL_IGRALEC.format(id_igralca=id_igralca)
    soup = pridobi_soup(url)
    if soup is None:
        return None
 
    podatki = {}
    podatki.update(pridobi_bio_igralca(soup))
    podatki.update(pridobi_statistiko_igralca(soup))
    return podatki



# -------------------------------------------------------------------
# funkcija, ki vrne seznam slovarjev s podatki vseh igralcev enega spola (vse ekipe skupaj)
# -------------------------------------------------------------------

def pridobi_vse_igralce(spol):

    ekipe = KONST.EKIPE_MOSKI if spol == "men" else KONST.EKIPE_ZENSKE

    vsi_igralci = []
 
    for id_ekipe, ime_drzave in ekipe.items():
        print(f"Berem ekipo: {ime_drzave} ...")  #izbrisi!!
        seznam_igralcev = pridobi_seznam_igralcev(spol, id_ekipe)
 
        for osnovni_podatki in seznam_igralcev:
            podrobni_podatki = pridobi_podatke_igralca(osnovni_podatki["id_igralca"])
            if podrobni_podatki is None:
                continue  # stran igralca se ni naložila, ga preskočimo
 
            igralec = {
                "drzava": ime_drzave,
                "st_dresa": osnovni_podatki["st_dresa"],
                "ime": osnovni_podatki["ime_na_seznamu"],
            }
            igralec.update(podrobni_podatki)
            vsi_igralci.append(igralec)
 
            time.sleep(0.5)
 
    return vsi_igralci