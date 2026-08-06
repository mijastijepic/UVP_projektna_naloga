# -----------------------------------------------------------------------
# UPORABNIŠKI POSREDNIK (User-Agent)
# -----------------------------------------------------------------------

GLAVE = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}



# -----------------------------------------------------------------------
# OSNOVNI NASLOVI (URL-ji) STRANI VOLLEYBALLWORLD.COM
# -----------------------------------------------------------------------

URL_IGRALCI_EKIPE = (
    "https://en.volleyballworld.com/volleyball/competitions/"
    "volleyball-nations-league/teams/{spol}/{id_ekipe}/players/"
)

URL_IGRALEC = (
    "https://en.volleyballworld.com/volleyball/competitions/"
    "volleyball-nations-league/players/{id_igralca}"
)



# -----------------------------------------------------------------------
# ID-JI EKIP ZA VNL 2026
# -----------------------------------------------------------------------

EKIPE_MOSKI = {
    8599: "Argentina",
    8600: "Belgium",
    8601: "Brazil",
    8602: "Bulgaria",
    8603: "Canada",
    8604: "China",
    8605: "Cuba",
    8606: "France",
    8607: "Germany",
    8608: "Iran",
    8609: "Italy",
    8610: "Japan",
    8611: "Poland",
    8612: "Slovenia",
    8613: "Serbia",
    8614: "Turkiye",
    8615: "Ukraine",
    8616: "USA",
}
 
EKIPE_ZENSKE = {
    8617: "Belgium",
    8618: "Brazil",
    8619: "Bulgaria",
    8620: "Canada",
    8621: "China",
    8622: "Czechia",
    8623: "Dominican Republic",
    8624: "France",
    8625: "Germany",
    8626: "Italy",
    8627: "Japan",
    8628: "Netherlands",
    8629: "Poland",
    8630: "Serbia",
    8631: "Thailand",
    8632: "Turkiye",
    8633: "Ukraine",
    8634: "USA",
}


# -----------------------------------------------------------------------
# PREVODI DRŽAV IN POZICIJ V SLOVENŠČINO
# -----------------------------------------------------------------------
 
SLOVAR_DRZAV = {
    "Argentina": "Argentina",
    "Belgium": "Belgija",
    "Brazil": "Brazilija",
    "Bulgaria": "Bolgarija",
    "Canada": "Kanada",
    "China": "Kitajska",
    "Cuba": "Kuba",
    "Czechia": "Češka",
    "Dominican Republic": "Dominikanska republika",
    "France": "Francija",
    "Germany": "Nemčija",
    "Iran": "Iran",
    "Italy": "Italija",
    "Japan": "Japonska",
    "Netherlands": "Nizozemska",
    "Poland": "Poljska",
    "Serbia": "Srbija",
    "Slovenia": "Slovenija",
    "Thailand": "Tajska",
    "Turkiye": "Turčija",
    "Ukraine": "Ukrajina",
    "USA": "ZDA",
}
 
SLOVAR_POZICIJ_MOSKI = {
    "Setter": "Podajalec",
    "Outside hitter": "Sprejemalec",
    "Middle blocker": "Srednji bloker",
    "Opposite spiker": "Korektor",
    "Libero": "Libero",
}
 
SLOVAR_POZICIJ_ZENSKE = {
    "Setter": "Podajalka",
    "Outside hitter": "Sprejemalka",
    "Middle blocker": "Srednja blokerka",
    "Opposite spiker": "Korektorica",
    "Libero": "Libero",
}


# -----------------------------------------------------------------------
# IMENA ZA STATISTIKO IGRALCA
# -----------------------------------------------------------------------

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