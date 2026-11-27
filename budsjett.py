"""
budsjett.py - Meny 6: Budsjett og personlig økonomi
---------------------------------------------------

Input:  inntekt per måned (etter skatt) og utgifter per kategori
Output: utgifter per kategori (beløp og andel av inntekt)
        sum utgifter, overskudd eller underskudd per måned og år
        enkle forslag til sparing eller hva som kan kuttes

Forutsetninger (fra oppgaven):
    - Budsjett for én måned. Per år = per måned * 12
    - Forhåndsdefinerte kategorier
    - Forslagene bygger på enkle regler: største utgiftspost,
      og at 10-20 % av inntekten bør spares
"""

from felles import skriv_overskrift, les_tall, formater_kr, formater_prosent, MAKS_BELOP

# De forhåndsdefinerte kategoriene brukeren fyller ut
KATEGORIER = [
    "Bolig",
    "Mat og dagligvarer",
    "Transport",
    "Strøm, internett og mobil",
    "Forsikringer",
    "Klær og personlig pleie",
    "Fritid",
    "Abonnementer",
    "Gjeld og kreditt",
    "Annet",
]

# Regler for forslagene (i prosent av inntekten)
SPAREMAAL_MIN_PROSENT = 10
SPAREMAAL_MAKS_PROSENT = 20
KUTT_PROSENT = 10   # Forslag: kutt 10 % i den største utgiftsposten


def les_utgifter():
    # Leser inn utgift for hver kategori. Returnerer et dictionary: kategori -> beløp
    print("\nSkriv inn utgifter per måned (trykk Enter for 0):")
    utgifter = {}
    for kategori in KATEGORIER:
        utgifter[kategori] = les_tall("  " + kategori + ": ", minimum=0, standard=0)
    return utgifter

def beregn_sum_utgifter(utgifter):
    # Legger sammen alle utgiftene
    sum_utgifter = 0
    for kategori in utgifter:
        sum_utgifter = sum_utgifter + utgifter[kategori]
    return sum_utgifter

def finn_storste_post(utgifter):
    # Finner kategorien med størst utgift. Returnerer navn og beløp
    storste_kategori = ""
    storste_belop = 0
    for kategori in utgifter:
        if utgifter[kategori] > storste_belop:
            storste_kategori = kategori
            storste_belop = utgifter[kategori]
    return storste_kategori, storste_belop

def vis_forslag(inntekt, rest, utgifter):
    # Skriver enkle forslag basert på reglene i oppgaven
    spareandel = rest / inntekt * 100
    sparemaal_min = inntekt * SPAREMAAL_MIN_PROSENT / 100
    sparemaal_maks = inntekt * SPAREMAAL_MAKS_PROSENT / 100

    print("FORSLAG")

    # Regel 1: Hvor mye er igjen til sparing?
    if rest < 0:
        print("  Du bruker mer enn du tjener. Utgiftene må ned med minst",
              formater_kr(-rest), "per måned.")
    elif spareandel < SPAREMAAL_MIN_PROSENT:
        print("  Du har bare", formater_prosent(spareandel, 1), "igjen av inntekten.")
        print("  Prøv å spare 10-20 %, altså mellom", formater_kr(sparemaal_min),
              "og", formater_kr(sparemaal_maks), "per måned.")
    elif spareandel < SPAREMAAL_MAKS_PROSENT:
        print("  Bra! Du kan spare", formater_prosent(spareandel, 1), "av inntekten.")
        print("  Prøv å nå 20 %, som er", formater_kr(sparemaal_maks), "per måned.")
    else:
        print("  Veldig bra! Du har", formater_prosent(spareandel, 1), "igjen.")
        print("  Sett gjerne av minst", formater_kr(sparemaal_maks),
              "til sparing hver måned.")

    # Regel 2: Største utgiftspost
    storste_kategori, storste_belop = finn_storste_post(utgifter)
    if storste_belop > 0:
        kutt = storste_belop * KUTT_PROSENT / 100
        print("  Største utgift er", storste_kategori, "med", formater_kr(storste_belop) + ".")
        print("  Kutter du 10 % her, sparer du", formater_kr(kutt), "i måneden og",
              formater_kr(kutt * 12), "i året.")

def vis_resultat(inntekt, utgifter):
    # Skriver ut utgifter, summer og forslag
    sum_utgifter = beregn_sum_utgifter(utgifter)
    rest = inntekt - sum_utgifter   # Positiv = overskudd, negativ = underskudd

    skriv_overskrift("Resultat - budsjett")

    print("UTGIFTER PER MÅNED (andel av inntekt)")
    for kategori in utgifter:
        belop = utgifter[kategori]
        if belop > 0:   # Viser bare kategorier brukeren har fylt ut
            andel = belop / inntekt * 100
            print(" ", kategori + ":", formater_kr(belop),
                  "(" + formater_prosent(andel, 1) + ")")
    print()

    print("OVERSIKT")
    print("  Inntekt per måned:  ", formater_kr(inntekt))
    print("  Utgifter per måned: ", formater_kr(sum_utgifter),
          "(" + formater_prosent(sum_utgifter / inntekt * 100, 1) + ")")
    if rest >= 0:
        print("  Overskudd per måned:", formater_kr(rest))
        print("  Overskudd per år:   ", formater_kr(rest * 12))
    else:
        print("  Underskudd per måned:", formater_kr(-rest))
        print("  Underskudd per år:   ", formater_kr(-rest * 12))
    print()

    vis_forslag(inntekt, rest, utgifter)

def kjor_budsjett():
    # Hovedfunksjon for budsjettkalkulatoren (kalles fra menyen)
    skriv_overskrift("Budsjett og personlig økonomi")
    inntekt = les_tall("Inntekt per måned etter skatt: ", minimum=1)
    utgifter = les_utgifter()
    vis_resultat(inntekt, utgifter)
