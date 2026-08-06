import re
import time
 
import requests
from bs4 import BeautifulSoup
 
import konstante as KONST


# -------------------------------------------------------------------
# funkcija, ki prenese spletno stran in jo pretvori v BeautifulSoup objekt
# -------------------------------------------------------------------

def pridobi_soup(url):

    try:
        odgovor = requests.get(url, headers=KONST.GLAVE, timeout=10)
        odgovor.raise_for_status()  # sproži napako, če stran ni bila najdena (npr. 404)

    except requests.RequestException as napaka:
        print(f"Napaka pri nalaganju strani {url}: {napaka}")
        return None
 
    return BeautifulSoup(odgovor.text, "html5lib")


# -------------------------------------------------------------------
# funkcija za prevajanje
# -------------------------------------------------------------------

def prevedi(izraz, slovar):

    if izraz is None:
        return None
    return slovar.get(izraz, izraz)  # če izraza ni v slovarju vrne kar nespremenjen izraz


# -------------------------------------------------------------------
# funkcija, ki pridobi seznam igralcev za eno ekipo
# -------------------------------------------------------------------

def pridobi_seznam_igralcev(spol, id_ekipe):

    """
    Za izbrano ekipo (spol = "men" ali "women", id_ekipe = številka ekipe iz
    konstante.py) prebere stran s seznamom igralcev in vrne seznam slovarjev
    z osnovnimi podatki o vsakem igralcu (ID, št. dresa, priimek).
    """

    url = KONST.URL_IGRALCI_EKIPE.format(spol=spol, id_ekipe=id_ekipe)

    soup = pridobi_soup(url)
    if soup is None:
        return []
 
    igralci = []

    # tabela z igralci je sestavljena iz vrstic <tr>, znotraj vsake pa so
    # tri celice <td>: številka dresa, priimek (s povezavo), pozicija
    for vrstica in soup.find_all("tr"):
        celice = vrstica.find_all("td")
        if len(celice) != 3:
            continue  # to ni vrstica z igralcem (npr. glava tabele)
 
        celica_priimka = celice[1]
        povezava = celica_priimka.find("a")
        if povezava is None or not povezava.get("href"):
            continue  # npr. trener - nima povezave na svojo stran, zato ga preskočimo

        ujemanje = re.search(r"(\d+)/?$", povezava["href"])  # ID igralca je zadnje zaporedje številk v povezavi (npr. .../players/151390)
        if ujemanje is None:
            continue
 
        igralci.append({
            "id_igralca": ujemanje.group(1),
            "st_dresa": celice[0].get_text(strip=True),  # strip=True odstrani odvečne presledke, prelome vrstic,...
            "priimek": celica_priimka.get_text(strip=True),
        })
        
    return igralci


# -------------------------------------------------------------------
# funkcija, ki zbere osebne podatke igralca (igralčev bio)
# -------------------------------------------------------------------

def ujemanje_oznake(besedilo, iskana_oznaka):

    if besedilo is None:
        return False
    return besedilo.strip() == iskana_oznaka

    """
    Funkcija vrednost_za_bio_oznako poišče vrednost v razdelku "Player Bio"
    glede na bio oznako (npr. "Age" ali "Position").

    HTML na strani je zgrajen tako, da ima vsak podatek svoj "stolpec" -
    v njem ima najprej oznako (npr. "Age"), nato pa isto vrednost dvakrat
    (enkrat polno "--desktop" za računalnik, enkrat skrajšano "--mobile"
    za telefon). Primer:

        <div class=vbw-player-bio-col>
            <div class=vbw-player-bio-head>Position</div>
            <div class="vbw-player-bio-text --desktop">Setter</div>
            <div class="vbw-player-bio-text --mobile">S</div>
        </div>
    """

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



def pridobi_bio_igralca(soup, spol):
    slovar_pozicij = KONST.SLOVAR_POZICIJ_MOSKI if spol == "men" else KONST.SLOVAR_POZICIJ_ZENSKE

    return {
        "pozicija": prevedi(vrednost_za_bio_oznako(soup, "Position"), slovar_pozicij),
        "starost": vrednost_za_bio_oznako(soup, "Age"),
        "datum_rojstva": vrednost_za_bio_oznako(soup, "Birth date"),
        "visina_cm": vrednost_za_bio_oznako(soup, "Height"),
    }


# -------------------------------------------------------------------
# funkcija, ki pridobi igralčevo statistiko iz razdelka "Player Competition Statistics".
# -------------------------------------------------------------------

def preveri_zacetek_statistike(besedilo):
    return ujemanje_oznake(besedilo, "Player Competition Statistics")
 
 
def pridobi_statistiko_igralca(soup):

    zacetna_oznaka = soup.find(string=preveri_zacetek_statistike)  # poiščemo naslov razdelka - če ga ni, igralec še ni odigral tekme
    if zacetna_oznaka is None:
        return {ime: None for ime in KONST.IMENA_STATISTIK} 
 
    stevilo_potrebnih_nizov = len(KONST.IMENA_STATISTIK) * 2
    nizi = []
    trenutni_element = zacetna_oznaka
 
    while len(nizi) < stevilo_potrebnih_nizov:
        trenutni_element = trenutni_element.find_next(string=True)

        if trenutni_element is None:
            break
        
        besedilo = trenutni_element.strip()

        if not besedilo:  # preskočimo prazne nize (presledki, prelomi vrstic), ki so v pythonu obravnavani kot False
            continue

        if besedilo == "%" and nizi:  # ker je znak "%" na strani zapisan kot svoj ločen niz, ga prilepimo na prejšnjo vrednost
            nizi[-1] += besedilo
        else:
            nizi.append(besedilo)
 
    vrednosti = nizi[1::2]
 
    statistika = {}
    for ime_statistike, vrednost in zip(KONST.IMENA_STATISTIK, vrednosti):
        statistika[ime_statistike] = vrednost
 
    return statistika


# -------------------------------------------------------------------
# funkcija, ki pridobi vse podatke enega igralca (bio + statistika skupaj)
# -------------------------------------------------------------------

def pridobi_podatke_igralca(id_igralca, spol):

    url = KONST.URL_IGRALEC.format(id_igralca=id_igralca)
    soup = pridobi_soup(url)
    if soup is None:
        return None
 
    podatki = {}
    podatki.update(pridobi_bio_igralca(soup, spol))
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
            podrobni_podatki = pridobi_podatke_igralca(osnovni_podatki["id_igralca"], spol)
            if podrobni_podatki is None:
                continue  # stran igralca se ni naložila, ga preskočimo
 
            igralec = {
                "drzava": prevedi(ime_drzave, KONST.SLOVAR_DRZAV),
                "st_dresa": osnovni_podatki["st_dresa"],
                "priimek": osnovni_podatki["priimek"],
            }
            igralec.update(podrobni_podatki)
            vsi_igralci.append(igralec)
 
            time.sleep(0.5)
 
    return vsi_igralci