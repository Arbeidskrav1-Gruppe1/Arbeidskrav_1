"""
veksel.py  -  Meny 2: Vekselautomat

Input:  varer (navn og pris) og betalt beløp
Output: total veksel og antall av hver seddel og mynt

Formler:
    veksel         = betalt - sum av prisene
    antall av enhet = veksel // verdi   (størst enhet først)
    resten          = veksel % verdi    (går videre til neste enhet)

Forutsetninger:
    - Veksel rundes til hele kroner (minste mynt er 1 kr).
    - Det gis tilbake færrest mulig sedler og mynter.
"""

from felles import skriv_overskrift, les_tall, les_ja_nei, formater_kr

ENHETER = [
    (1000, "tusenlapp"), (500, "femhundrelapp"), (200, "tohundrelapp"),
    (100, "hundrelapp"), (50, "femtilapp"), (20, "tjuekrone"),
    (10, "tikrone"), (5, "femkrone"), (1, "enkrone")
]

def beregn_veksel(veksel_kr):
    # Deler veksel på seddel- og myntverdier, størst først
    veksel = round(veksel_kr)  # Minste mynt er 1 kr, så vi runder til hele kroner
    resultat = []

    for enhet in ENHETER:
        antall = veksel // enhet[0]
        veksel %= enhet[0]
        resultat.append([enhet[0], enhet[1], antall])

    # Returnerer en liste med [verdi, navn, antall] for hver enhet
    return resultat

def les_varer():
    # Leser inn varer til brukeren er ferdig. Hver vare lagres som [navn, pris]
    varer = []
    while True:

        navn = input("Skriv navn på varen: ")
        pris = les_tall("Pris: ", minimum=0)
        varer.append([navn, pris])
        print()
        if not les_ja_nei("Vil du legge til en vare til? (j/n): "):
            break
    return varer


def vis_resultat(varer, betalt, veksel_kr, resultat):
    # Skriver ut varene, betalt beløp, veksel og antall av hver seddel og mynt
    skriv_overskrift("Resultat - vekselautomat")
    for vare in varer:
        print(vare[0] + ":", formater_kr(vare[1]))
    print()
    print("Betalt:", formater_kr(betalt))
    print("Veksel:", formater_kr(veksel_kr))
    print()

    for enhet in resultat:
        print(enhet[2], "x", enhet[1])

def kjor_vekselautomat():
    skriv_overskrift("Vekselautomat")
    varer = les_varer()

    total = 0
    for vare in varer:
        total = total + vare[1]
    print()
    print("Totalpris:", formater_kr(total))

    betalt = les_tall("Hvor mye betaler du med: ", minimum=total)
    veksel_kr = betalt - total
    vis_resultat(varer, betalt, veksel_kr, beregn_veksel(veksel_kr))