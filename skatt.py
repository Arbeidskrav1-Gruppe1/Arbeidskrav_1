"""
skatt.py  -  Meny 7: Skattekalkulator
-------------------------------------

Input:  brutto årsinntekt (lønn) og eventuelle andre fradrag
Output: skatt fordelt på skatt på alminnelig inntekt (22 %), trinnskatt
        og trygdeavgift (7,6 %), total skatt, effektiv skattesats,
        og netto per år og per måned sammenlignet med brutto

Forenklet modell for lønnsinntekt, én person, inntektsåret 2026.
Satsene er hentet fra Skatteetaten / Finansdepartementet (skattesatser 2026).

Slik regnes skatten:
1. Minstefradrag = 46 % av lønn, men maks 95 700 kr
2. Alminnelig inntekt = lønn - minstefradrag - andre fradrag
3. Skatt på alminnelig inntekt = 22 % av (alminnelig inntekt - personfradrag)
4. Trinnskatt regnes av brutto lønn, trinn for trinn
5. Trygdeavgift = 7,6 % av brutto lønn
   (ingen avgift under 99 650 kr, og maks 25 % av det som er over grensen)
"""

from felles import skriv_overskrift, les_tall, formater_kr, formater_prosent

# Skattesatser 2026
SKATT_ALMINNELIG_PROSENT = 22
PERSONFRADRAG = 114540
MINSTEFRADRAG_PROSENT = 46
MINSTEFRADRAG_MAKS = 95700
TRYGDEAVGIFT_PROSENT = 7.6
TRYGDEAVGIFT_NEDRE_GRENSE = 99650
TRYGDEAVGIFT_MAKS_PROSENT = 25

# Trinnskatt: innslagspunkt og sats for hvert trinn (samme plass i listene hører sammen)
TRINN_GRENSER = [226100, 318300, 725050, 980100, 1467200]
TRINN_SATSER = [1.7, 4.0, 13.7, 16.8, 17.8]


def beregn_minstefradrag(lonn):
    # 46 % av lønn, men aldri mer enn maksbeløpet
    minstefradrag = lonn * MINSTEFRADRAG_PROSENT / 100
    if minstefradrag > MINSTEFRADRAG_MAKS:
        minstefradrag = MINSTEFRADRAG_MAKS
    return minstefradrag


def beregn_trinnskatt(lonn):
    """
    Regner trinnskatt trinn for trinn.
    Hvert trinn gjelder fra sin grense opp til neste trinns grense.
    """
    trinnskatt = 0

    for i in range(len(TRINN_GRENSER)):
        nedre_grense = TRINN_GRENSER[i]

        # Lønnen når ikke opp til dette trinnet
        if lonn <= nedre_grense:
            break

        # Øvre grense er neste trinn, eller lønnen selv hvis vi er på siste trinn
        if i < len(TRINN_GRENSER) - 1:
            ovre_grense = TRINN_GRENSER[i + 1]
        else:
            ovre_grense = lonn

        # Er lønnen lavere enn øvre grense, skattes bare opp til lønnen
        if lonn < ovre_grense:
            ovre_grense = lonn

        belop_i_trinnet = ovre_grense - nedre_grense
        trinnskatt = trinnskatt + belop_i_trinnet * TRINN_SATSER[i] / 100

    return trinnskatt

def beregn_trygdeavgift(lonn):
    # 7,6 % av lønn. Ingen avgift under grensen, og en øvre grense for lave lønner
    if lonn <= TRYGDEAVGIFT_NEDRE_GRENSE:
        return 0

    trygdeavgift = lonn * TRYGDEAVGIFT_PROSENT / 100
    maks_avgift = (lonn - TRYGDEAVGIFT_NEDRE_GRENSE) * TRYGDEAVGIFT_MAKS_PROSENT / 100
    if trygdeavgift > maks_avgift:
        trygdeavgift = maks_avgift
    return trygdeavgift

def beregn_skatt(lonn, andre_fradrag):
    # Regner ut alle delene av skatten og returnerer dem
    minstefradrag = beregn_minstefradrag(lonn)

    alminnelig_inntekt = lonn - minstefradrag - andre_fradrag
    if alminnelig_inntekt < 0:
        alminnelig_inntekt = 0

    grunnlag = alminnelig_inntekt - PERSONFRADRAG
    if grunnlag < 0:
        grunnlag = 0

    skatt_alminnelig = grunnlag * SKATT_ALMINNELIG_PROSENT / 100
    trinnskatt = beregn_trinnskatt(lonn)
    trygdeavgift = beregn_trygdeavgift(lonn)

    return minstefradrag, alminnelig_inntekt, skatt_alminnelig, trinnskatt, trygdeavgift

def vis_resultat(lonn, andre_fradrag, minstefradrag, alminnelig_inntekt,
                 skatt_alminnelig, trinnskatt, trygdeavgift):
    # Skriver ut fradrag, skatt og netto inntekt
    total_skatt = skatt_alminnelig + trinnskatt + trygdeavgift
    netto = lonn - total_skatt

    effektiv_sats = 0
    if lonn > 0:
        effektiv_sats = total_skatt / lonn * 100

    skriv_overskrift("Resultat - skatt 2026")

    print("FRADRAG")
    print("  Minstefradrag:     ", formater_kr(minstefradrag))
    print("  Personfradrag:     ", formater_kr(PERSONFRADRAG))
    print("  Andre fradrag:     ", formater_kr(andre_fradrag))
    print("  Alminnelig inntekt:", formater_kr(alminnelig_inntekt))
    print()

    print("SKATT")
    print("  Skatt på alminnelig inntekt (22 %):", formater_kr(skatt_alminnelig))
    print("  Trinnskatt:                        ", formater_kr(trinnskatt))
    print("  Trygdeavgift (7,6 %):              ", formater_kr(trygdeavgift))
    print("  Total skatt:                       ", formater_kr(total_skatt))
    print("  Effektiv skattesats:               ", formater_prosent(effektiv_sats))
    print()

    print("BRUTTO OG NETTO")
    print("  Brutto per år:    ", formater_kr(lonn))
    print("  Brutto per måned: ", formater_kr(lonn / 12))
    print("  Netto per år:     ", formater_kr(netto))
    print("  Netto per måned:  ", formater_kr(netto / 12))
    print()
    print("Du betaler", formater_kr(total_skatt), "i skatt og sitter igjen med",
          formater_kr(netto), "av", formater_kr(lonn) + ".")

def kjor_skattekalkulator():
    # Hovedfunksjon for skattekalkulatoren (kalles fra menyen)
    skriv_overskrift("Skattekalkulator 2026")
    lonn = les_tall("Brutto årsinntekt: ", minimum=0)
    andre_fradrag = les_tall("Andre fradrag, f.eks. rentefradrag (Enter = 0): ",
                             minimum=0, standard=0)

    minstefradrag, alminnelig_inntekt, skatt_alminnelig, trinnskatt, trygdeavgift = \
        beregn_skatt(lonn, andre_fradrag)

    vis_resultat(lonn, andre_fradrag, minstefradrag, alminnelig_inntekt,
                 skatt_alminnelig, trinnskatt, trygdeavgift)
