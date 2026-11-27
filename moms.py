"""
moms.py - Meny 1: Momskalkulator
--------------------------------

Input:  for hver vare: navn, beløp, inkl./ekskl. mva og momskategori
Output: for hver vare: beløp ekskl. mva, mva-beløp og beløp inkl. mva
        samlet sum og mva-sum per momssats

Formler:
    inkl. mva  = ekskl. mva * (1 + sats/100)
    ekskl. mva = inkl. mva / (1 + sats/100)
    mva        = inkl. mva - ekskl. mva
"""

from felles import skriv_overskrift, les_tall, les_heltall, les_ja_nei, formater_kr

# De fire momssatsene oppgaven krever (i prosent)
MVA_SATSER = [25, 15, 12, 0]

def beregn_mva(belop, sats_prosent, er_inkl_mva):
    # Regner ut beløp ekskl. mva, mva-beløp og beløp inkl. mva for én vare
    if er_inkl_mva:
        belop_inkl = belop
        belop_ekskl = belop / (1 + sats_prosent / 100)
    else:
        belop_ekskl = belop
        belop_inkl = belop * (1 + sats_prosent / 100)

    mva_belop = belop_inkl - belop_ekskl
    return belop_ekskl, mva_belop, belop_inkl

def velg_sats():
    # Lar brukeren velge momskategori og returnerer satsen i prosent
    print("Momskategorier:")
    print("  1: 25 % (alminnelig sats)")
    print("  2: 15 % (mat og drikke)")
    print("  3: 12 % (transport, kino, hotell)")
    print("  4:  0 % (f.eks. bøker og aviser)")
    valg = les_heltall("Velg kategori (1-4): ", minimum=1, maksimum=4)
    return MVA_SATSER[valg - 1]   # Valg 1 er plass 0 i listen

def les_varer():
    # Leser inn én eller flere varer. Returnerer en liste med varer
    varer = []

    while True:
        print()
        navn = input("Navn på vare: ")
        belop = les_tall("Beløp: ", minimum=0)
        er_inkl_mva = les_ja_nei("Er beløpet inkludert mva? (j/n): ")
        sats_prosent = velg_sats()

        belop_ekskl, mva_belop, belop_inkl = beregn_mva(belop, sats_prosent, er_inkl_mva)

        # Hver vare lagres som en liste: [navn, sats, ekskl., mva, inkl.]
        varer.append([navn, sats_prosent, belop_ekskl, mva_belop, belop_inkl])

        if not les_ja_nei("\nVil du legge til en vare til? (j/n): "):
            break

    return varer

def vis_resultat(varer):
    # Skriver ut hver vare, samlet sum og mva per sats
    skriv_overskrift("Resultat - moms")

    sum_ekskl = 0
    sum_mva = 0
    sum_inkl = 0
    # Ett "regnestykke" per sats, starter på 0
    mva_per_sats = {25: 0, 15: 0, 12: 0, 0: 0}

    for vare in varer:
        navn, sats_prosent, belop_ekskl, mva_belop, belop_inkl = vare

        print(navn, "(" + str(sats_prosent) + " % mva)")
        print("  Ekskl. mva:", formater_kr(belop_ekskl))
        print("  Mva:       ", formater_kr(mva_belop))
        print("  Inkl. mva: ", formater_kr(belop_inkl))
        print()

        sum_ekskl = sum_ekskl + belop_ekskl
        sum_mva = sum_mva + mva_belop
        sum_inkl = sum_inkl + belop_inkl
        mva_per_sats[sats_prosent] = mva_per_sats[sats_prosent] + mva_belop

    print("SAMLET SUM")
    print("  Ekskl. mva:", formater_kr(sum_ekskl))
    print("  Mva:       ", formater_kr(sum_mva))
    print("  Inkl. mva: ", formater_kr(sum_inkl))
    print()

    print("MVA PER SATS")
    for sats_prosent in MVA_SATSER:
        print(" ", sats_prosent, "%:", formater_kr(mva_per_sats[sats_prosent]))

def kjor_momskalkulator():
    # Hovedfunksjon for momskalkulatoren (kalles fra menyen)
    skriv_overskrift("Momskalkulator")
    varer = les_varer()
    vis_resultat(varer)
