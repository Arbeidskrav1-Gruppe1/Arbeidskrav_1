"""
inflasjon.py  -  Meny 3: Inflasjonskalkulator

Input:  beløp i dag, antall år og inflasjon for hvert år (%)
Output: utvikling år for år, fremtidig pris, kjøpekraft i dagens kroner
        og samlet prisstigning

Formler:
    prisfaktor          = prisfaktor * (1 + inflasjon / 100)   (starter på 1)
    fremtidig pris      = beløp * prisfaktor
    kjøpekraft          = beløp / prisfaktor
    samlet prisstigning = (prisfaktor - 1) * 100

Forutsetninger:
    - Inflasjonen kan variere fra år til år. Brukeren kan også velge
      samme inflasjon for alle årene, så slipper man å skrive den mange ganger.
    - Negativ inflasjon er lov, men ikke lavere enn -50 %.
    - Fremtidig pris: hva noe som koster beløpet i dag, vil koste om x år.
    - Kjøpekraft: hva beløpet er verdt om x år, målt i dagens kroner.
"""

from felles import skriv_overskrift, skriv_linje, les_tall, les_heltall, les_ja_nei, formater_kr, formater_prosent, MAKS_BELOP

MAKS_AAR = 100
MIN_INFLASJON = -50  # Grensene stopper tulle input
MAKS_INFLASJON = 100

def les_inflasjon():
    # Leser inn beløpet og inflasjonen for hvert år. Inflasjonene lagres i en liste
    belop = les_tall("Skriv beløpet i dag: ", minimum=0, maksimum=MAKS_BELOP)
    antall_aar = les_heltall("Skriv antall år: ", minimum=1, maksimum=MAKS_AAR)

    inflasjoner = []
    if les_ja_nei("Er inflasjonen lik hvert år? (j/n): "):
        inflasjon = les_tall("Skriv inflasjon per år i %: ", minimum=MIN_INFLASJON, maksimum=MAKS_INFLASJON)
        for aar in range(antall_aar):
            inflasjoner.append(inflasjon)
    else:
        for aar in range(1, antall_aar + 1):
            inflasjon = les_tall("Skriv inflasjon for år " + str(aar) + " i %: ",
                                 minimum=MIN_INFLASJON, maksimum=MAKS_INFLASJON)
            inflasjoner.append(inflasjon)

    return belop, inflasjoner

def beregn_inflasjon(belop, inflasjoner):
    # Regner ut ett år om gangen. Hver rad lagres som [aar, inflasjon, pris, kjopekraft]
    # Returnerer alle radene og samlet prisstigning i prosent
    prisfaktor = 1  # 1 betyr samme pris som i dag. 1,03 betyr 3 % dyrere enn i dag
    utvikling = []
    aar = 1

    for inflasjon in inflasjoner:
        # Inflasjonen regnes av fjorårets pris, ikke dagens, så prisstigningen hoper seg opp
        prisfaktor = prisfaktor * (1 + inflasjon / 100)
        pris = belop * prisfaktor
        # Når prisene stiger, får man mindre for samme beløp, derfor deler vi
        kjopekraft = belop / prisfaktor
        utvikling.append([aar, inflasjon, pris, kjopekraft])
        aar += 1

    # Eksempel: prisfaktor 1,0599 gir (1,0599 - 1) * 100 = 5,99 %
    samlet_prisstigning = (prisfaktor - 1) * 100
    return utvikling, samlet_prisstigning

def vis_utvikling(utvikling):
    # Skriver ut tabellen år for år
    skriv_overskrift("Utvikling år for år")
    print("År".center(8) + "Inflasjon".center(14) + "Pris".center(25) + "Kjøpekraft".center(25))
    skriv_linje()

    for rad in utvikling:
        print(str(rad[0]).center(8) + formater_prosent(rad[1]).center(14)
              + formater_kr(rad[2]).center(25) + formater_kr(rad[3]).center(25))

def vis_resultat(belop, utvikling, samlet_prisstigning):
    # Skriver ut sluttresultatet. utvikling[-1] er siste år
    siste = utvikling[-1]
    antall_aar = siste[0]

    skriv_overskrift("Resultat - inflasjon")
    print("Beløp i dag:", formater_kr(belop))
    print("Pris om", antall_aar, "år:", formater_kr(siste[2]))
    print("Kjøpekraft om", antall_aar, "år (i dagens kroner):", formater_kr(siste[3]))
    print("Samlet prisstigning:", formater_prosent(samlet_prisstigning))

def kjor_inflasjonskalkulator():
    skriv_overskrift("Inflasjonskalkulator")
    belop, inflasjoner = les_inflasjon()

    utvikling, samlet_prisstigning = beregn_inflasjon(belop, inflasjoner)

    vis_utvikling(utvikling)
    vis_resultat(belop, utvikling, samlet_prisstigning)
