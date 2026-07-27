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