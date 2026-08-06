# UVP_projektna_naloga

Za projektno nalogo sem se odločila iz interneta pridobiti podatke in statistiko igralcev letošnjega odbojkarskega turnirja Volleyball Nations League - VNL 2026. Projektna avtomatsko pridobi podatke o igralcih in igralkah (tako moški kot ženske) s spletne strani https://en.volleyballworld.com/volleyball/competitions/volleyball-nations-league/, za vsakega igralca zbere osebne podatke (starost, višina, pozicija,...) in njegovo statistiko (točke iz napada, bloka, servisa,...). Podatki se shranijo v dve CSV datoteki, ki omogočata nadaljnjo analizo.

## Struktura projekta

```
UVP_projektna_naloga/
│
├── main.py                    # glavna datoteka - poganja cel program
├── pridobivanje_podatkov.py   # funkcije za scraping (ekipe, igralci, statistika)
├── konstante.py               # uporabniški posrednik, URL-ji, ID-ji ekip, slovarji prevodov
│
├── igralci_moski.csv          # zajeti podatki - moški
├── igralci_zenske.csv         # zajeti podatki - ženske
│
└── analiza_podatkov.ipynb     # analiza podatkov in grafi

```

## Opis delovanja

V datoteki `pridobivanje_podatkov.py` sem sestavila funkcije, ki iz spletne strani volleyballworld.com izluščijo podatke o igralcih VNL 2026. Funkcija `pridobi_seznam_igralcev` za izbrano ekipo prebere seznam igralcev (ime, št. dresa, pozicijo in ID), `pridobi_bio_igralca` in `pridobi_statistiko_igralca` pa za posameznega igralca prebereta še njegove osebne podatke (starost, višina, pozicija) in statistiko za letošnjo sezono (točke iz napada, bloka, servisa ter njihova učinkovitost v teh elementih). Ker so nekateri podatki na strani zapisani z manjkajočimi zapiralnimi značkami, sem za branje HTML-ja namesto vgrajenega `html.parser` uporabila knjižnico `html5lib`, ki HTML pravilno "sestavi" enako kot pravi brskalnik.

Imena držav in pozicij, ki jih stran vrača v angleščini, sem s pomočjo slovarjev iz `konstante.py` in funkcije `prevedi` prevedla v slovenščino - ločeno za moške in ženske pozicije (npr. "Podajalec"/"Podajalka").

Vse funkcije se povežejo v `pridobi_vse_igralce`, ki gre čez vse ekipe izbranega spola in za vsakega igralca zbere celoten nabor podatkov. To funkcijo nato pokličem v glavni datoteki `main.py`, ki podatke za moške in ženske shrani v ločeni CSV datoteki (`igralci_moski.csv`, `igralci_zenske.csv`).

Zbrane podatke sem nato uvozila v zvezek `analiza_podatkov.ipynb`, kjer sem jih očistila, analizirala in predstavila s tabelami in grafi.

## Navodila za zagon

Če bi želeli program pognati sami, je dovolj da zaženete datoteko `main.py`. Ta samodejno ustvari datoteki `igralci_moski.csv` in `igralci_zenske.csv`, ki sta potrebni za nadaljno analizo. Nato odprete datoteko `analiza_podatkov.ipynb` izvedete analizo.
