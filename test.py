import pridobivanje_podatkov as pp

igralci_slo = pp.pridobi_seznam_igralcev("men", 8612)
print(f"Najdenih igralcev: {len(igralci_slo)}")
print(igralci_slo)


prvi_igralec = igralci_slo[0]
print(f"Preverjam igralca: {prvi_igralec['ime_na_seznamu']} (ID: {prvi_igralec['id_igralca']})")

podatki = pp.pridobi_podatke_igralca(prvi_igralec["id_igralca"])
print(podatki)