import csv
 
import pridobivanje_podatkov as pp


# -------------------------------------------------------------------
# funkcija, ki shrani podatke v csv
# -------------------------------------------------------------------

def shrani_v_csv(igralci, ime_datoteke):

    """
    Shrani seznam slovarjev (en slovar = en igralec) v CSV datoteko.
    Imena stolpcev v CSV-ju vzame kar iz ključev prvega igralca na seznamu.
    """

    if not igralci:
        print(f'Opozorilo: ni podatkov za shranjevanje v {ime_datoteke}.')
        return

    imena_stolpcev = list(igralci[0].keys())

    with open(ime_datoteke, 'w', newline='', encoding='utf-8') as dat:
        csv_pisec = csv.DictWriter(dat, fieldnames=imena_stolpcev)
        csv_pisec.writeheader()
        csv_pisec.writerows(igralci)


# -------------------------------------------------------------------
# glavna funkcija
# -------------------------------------------------------------------

def main():
    print('Berem podatke za VNL-MOŠKI 2026 ...')
    moski_igralci = pp.pridobi_vse_igralce('men')
    shrani_v_csv(moski_igralci, 'igralci_moski.csv')
 
    print('\nBerem podatke za VNL-ŽENSKE 2026 ...')
    zenske_igralke = pp.pridobi_vse_igralce('women')
    shrani_v_csv(zenske_igralke, 'igralci_zenske.csv')
 
    print('\nKonec. Podatki so shranjeni.')


# Naslednja funkcija poskrbi, da se main() požene SAMO, če je ta datoteka pognana
# neposredno (python main.py), ne pa tudi, če bi jo kdo uvozil v drugo datoteko.
if __name__ == '__main__':  
    main()