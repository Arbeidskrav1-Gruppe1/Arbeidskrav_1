"""
sparing.py  -  Meny 4: Sparekalkulator

Input:  startbeløp, månedlig sparebeløp, årlig rente (%) og antall år
Output: innskudd, renter og saldo år for år, sluttsum,
        totalt innskudd og totalt opptjent rente

Formler (regnes for hver måned):
    månedsrente = årlig rente / 12
    rente       = saldo * månedsrente / 100
    saldo       = saldo + rente + månedlig sparebeløp

Forutsetninger:
    - Fast rente hele perioden.
    - Renten legges til hver måned (årsrente / 12).
    - Renten regnes før månedens innskudd, altså regnes innskuddet
      som satt inn på slutten av måneden.
    - Ingen skatt eller gebyrer.
"""

from felles import skriv_overskrift, skriv_linje, les_tall, les_heltall, formater_kr, MAKS_BELOP, MAANEDER_PER_AAR

MAKS_AAR = 100
MAKS_RENTE = 30  # Grensen stopper tullete input

def les_sparing():
    # Leser inn verdiene beregningen bygger på
    startbelop = les_tall("Skriv startbeløp: ", minimum=0, maksimum=MAKS_BELOP)
    maanedlig_sparing = les_tall("Skriv månedlig sparebeløp: ", minimum=0, maksimum=MAKS_BELOP)
    rente_prosent = les_tall("Skriv årlig rente i %: ", minimum=0, maksimum=MAKS_RENTE)
    antall_aar = les_heltall("Skriv antall år: ", minimum=1, maksimum=MAKS_AAR)

    return startbelop, maanedlig_sparing, rente_prosent, antall_aar

def beregn_sparing(startbelop, maanedlig_sparing, rente_prosent, antall_aar):
    # Regner ut én måned om gangen, og lagrer én rad per år som [aar, innskudd, renter, saldo]
    # Returnerer alle radene og totalt opptjent rente
    maanedsrente = rente_prosent / MAANEDER_PER_AAR
    saldo = startbelop
    total_rente = 0
    utvikling = []

    for aar in range(1, antall_aar + 1):
        innskudd_i_aar = 0  # Nullstilles hvert år, så tabellen viser tallene for akkurat det året
        renter_i_aar = 0

        for maaned in range(MAANEDER_PER_AAR):
            # Renten regnes før innskuddet, så månedens innskudd får ikke rente før neste måned
            rente = saldo * maanedsrente / 100
            # Renten legges til saldoen, så neste måned får man rente på renten (renters rente)
            saldo = saldo + rente + maanedlig_sparing
            renter_i_aar += rente
            innskudd_i_aar += maanedlig_sparing

        total_rente += renter_i_aar
        utvikling.append([aar, innskudd_i_aar, renter_i_aar, saldo])

    return utvikling, total_rente

def vis_utvikling(utvikling):
    # Skriver ut tabellen år for år
    skriv_overskrift("Utvikling år for år")
    print("År".center(8) + "Innskudd".center(20) + "Renter".center(20) + "Saldo".center(24))
    skriv_linje()

    for rad in utvikling:
        print(str(rad[0]).center(8) + formater_kr(rad[1]).center(20)
              + formater_kr(rad[2]).center(20) + formater_kr(rad[3]).center(24))

def vis_resultat(startbelop, utvikling, total_rente):
    # Skriver ut sluttsum, totalt innskudd og totalt opptjent rente. utvikling[-1] er siste år
    siste = utvikling[-1]

    # Totalt innskudd er startbeløpet pluss alt som er satt inn hvert år (rad[1])
    totalt_innskudd = startbelop
    for rad in utvikling:
        totalt_innskudd += rad[1]

    skriv_overskrift("Resultat - sparing")
    print("Sluttsum etter", siste[0], "år:", formater_kr(siste[3]))
    print("Totalt innskudd (med startbeløp):", formater_kr(totalt_innskudd))
    print("Totalt opptjent rente:", formater_kr(total_rente))

def kjor_sparekalkulator():
    skriv_overskrift("Sparekalkulator")
    startbelop, maanedlig_sparing, rente_prosent, antall_aar = les_sparing()

    utvikling, total_rente = beregn_sparing(startbelop, maanedlig_sparing, rente_prosent, antall_aar)

    vis_utvikling(utvikling)
    vis_resultat(startbelop, utvikling, total_rente)
