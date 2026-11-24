"""
pensjon.py  -  Meny 8: Pensjon og livslønn

Input:  startalder, pensjonsalder, årlig startlønn, årlig lønnsvekst (%),
        pensjonssparing (% av lønn) og forventet årlig avkastning (%)
Output: lønnsutvikling over yrkeslivet (år for år, eller utvalgte år),
        samlet inntekt, estimert pensjonsbeholdning ved pensjonsalder,
        og estimert pensjon per år og per måned

Formler:
    lønn første år      = startlønn
    lønn neste år       = lønn * (1 + vekst / 100)
    sparing per år      = lønn * sparing_prosent / 100
    beholdning per år   = (beholdning + sparing) * (1 + avkastning / 100)
    samlet inntekt      = summen av lønnen i alle årene
    pensjon per år      = beholdning / (uttaksalder - pensjonsalder)
    pensjon per måned   = pensjon per år / 12

Forutsetninger:
    - Du jobber fra startalder til pensjonsalder
      (antall år = pensjonsalder - startalder).
    - Årets sparing legges til beholdningen, og deretter får hele
      beholdningen avkastning for det året.
    - Fast lønnsvekst og fast avkastning hele perioden.
    - Pensjonen tas ut jevnt fra pensjonsalder til uttaksalder på 85 år.
    - Forenklet modell: NAV/folketrygd regnes ikke med, og det er ingen skatt.
"""

from felles import skriv_overskrift, skriv_linje, les_tall, les_heltall, formater_kr, formater_prosent, skriv_maaned_og_aar_overskrift, skriv_maaned_og_aar, MAKS_BELOP

UTTAKSALDER = 85

def les_pensjon():
    startalder = les_heltall("Skriv startalder: ", minimum=16, maksimum=UTTAKSALDER - 2)
    pensjonsalder = les_heltall("Skriv pensjonsalder: ", minimum=startalder + 1, maksimum=UTTAKSALDER - 1)
    startlonn = les_tall("Skriv din årlige startlønn: ", minimum=0, maksimum=MAKS_BELOP) #Grense for å stoppe tulle input
    lonnsvekst = les_tall("Skriv din årlige lønnsvekst i %: ", minimum=0, maksimum=20) #Grense for å stoppe tulle input
    pensjonssparing_prosent = les_tall("Skriv din pensjonssparing av lønnen din i %: ", minimum=0, maksimum=100)
    avkastning = les_tall("Skriv inn forventet årlig avkastning i %: ", minimum=0, maksimum=30) #Grense for å stoppe tulle input

    return startalder, pensjonsalder, startlonn, lonnsvekst, pensjonssparing_prosent, avkastning

def les_visning(startalder, pensjonsalder):
    start_visning = les_heltall(
        "Vis fra alder (Enter for alle): ",
        minimum=startalder, maksimum=pensjonsalder-1, standard=startalder)

    stopp_visning = les_heltall(
        "Vis til alder (Enter for alle): ",
        minimum=start_visning, maksimum=pensjonsalder - 1, standard=pensjonsalder - 1)

    return start_visning, stopp_visning

def beregn_lonnsutvikling(startalder, pensjonsalder, startlonn, lonnsvekst, pensjonssparing_prosent, avkastning):
    lonn = startlonn
    beholdning = 0
    samlet_inntekt = 0
    lonnsutvikling = []

    for alder in range(startalder, pensjonsalder):
        sparing = lonn * pensjonssparing_prosent / 100
        beholdning = (beholdning + sparing) * (1 + avkastning / 100)
        lonnsutvikling.append([alder, lonn, sparing, beholdning])
        samlet_inntekt += lonn
        lonn = lonn * (1 + lonnsvekst / 100)

    return lonnsutvikling, samlet_inntekt

def beregn_pensjon(beholdning, pensjonsalder):
    aar_med_pensjon = UTTAKSALDER - pensjonsalder
    pensjon_per_aar = beholdning / aar_med_pensjon

    return pensjon_per_aar

def vis_lonnsutvikling(lonnsutvikling, start_visning, stopp_visning):
    skriv_overskrift("Lønnsutvikling")
    print("Alder".center(8) + "Lønn".center(20) + "Sparing".center(20) + "Beholdning".center(24))
    skriv_linje()

    for aar in lonnsutvikling:
        if aar[0] >= start_visning and aar[0] <= stopp_visning:
            print(str(aar[0]).center(8) + formater_kr(aar[1]).center(20) + formater_kr(aar[2]).center(20) + formater_kr(aar[3]).center(24))

def vis_resultat(samlet_inntekt, beholdning, pensjon_per_aar):
    skriv_overskrift("Resultat")
    print("Samlet inntekt:", formater_kr(samlet_inntekt))
    print("Pensjonsbeholdning:", formater_kr(beholdning))

    skriv_maaned_og_aar_overskrift()
    skriv_maaned_og_aar("Pensjon", pensjon_per_aar)

def kjor_pensjonskalkulator():
    startalder, pensjonsalder, startlonn, lonnsvekst, pensjonssparing_prosent, avkastning = les_pensjon()

    lonnsutvikling, samlet_inntekt = beregn_lonnsutvikling(
        startalder, pensjonsalder, startlonn, lonnsvekst, pensjonssparing_prosent, avkastning)

    pensjon_per_aar = beregn_pensjon(lonnsutvikling[-1][3], pensjonsalder)

    start_visning, stopp_visning = les_visning(startalder, pensjonsalder)

    vis_lonnsutvikling(lonnsutvikling, start_visning, stopp_visning)

    vis_resultat(samlet_inntekt, lonnsutvikling[-1][3], pensjon_per_aar)