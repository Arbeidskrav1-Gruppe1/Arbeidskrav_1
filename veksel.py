"""
Inputs:
Pris og innbetalt beløp 

Output:
Totalt beløp tilbake 
Antall av hver seddel og mynt som gis tilbake 
"""

from felles import skriv_overskrift, les_tall, les_ja_nei, formater_kr

def beregn_veksel(veksel_kr):

    veksel = round(veksel_kr)

    tusen_lapper = veksel // 1000
    veksel %= 1000

    femhundre_lapper = veksel // 500
    veksel %= 500

    tohundre_lapper = veksel // 200
    veksel %= 200

    hundre_lapper = veksel // 100
    veksel %= 100

    femti_lapper = veksel // 50
    veksel %= 50

    tjue_kroner = veksel // 20
    veksel %= 20

    ti_kroner = veksel // 10
    veksel %= 10

    fem_kroner = veksel // 5
    en_kroner = veksel % 5

    return [tusen_lapper, femhundre_lapper, tohundre_lapper, hundre_lapper,
            femti_lapper, tjue_kroner, ti_kroner, fem_kroner, en_kroner]

def les_varer():
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
    skriv_overskrift("Resultat - vekselautomat")
    for vare in varer:
        print(vare[0] + ":", formater_kr(vare[1]))
    print()
    print("Betalt:", formater_kr(betalt))
    print("Veksel:", formater_kr(veksel_kr))
    print()

    print(resultat[0], "x tusenlapp")
    print(resultat[1], "x femhundrelapp")
    print(resultat[2], "x tohundrelapp")
    print(resultat[3], "x hundrelapp")
    print(resultat[4], "x femtilapp")
    print(resultat[5], "x tjuekrone")
    print(resultat[6], "x tikrone")
    print(resultat[7], "x femkrone")
    print(resultat[8], "x enkrone")

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