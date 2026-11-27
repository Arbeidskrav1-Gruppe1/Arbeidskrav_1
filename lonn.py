"""
lonn.py  -  Meny 5: Lønnskalkulator

Input:  timelønn, arbeidstimer per uke, overtidstimer per måned,
        overtidstillegg (%) og skatteprosent
Output: ordinær lønn, overtid, lønn før skatt (brutto), skattetrekk og
        lønn etter skatt (netto), alt per måned og per år
        nøkkeltall: overtidstimelønn, overtid av brutto (%) og netto per time

Formler:
    ordinær lønn per år = timelønn * timer per uke * 52
    overtid per år      = timelønn * (1 + tillegg / 100) * overtidstimer * 12
    brutto per år       = ordinær lønn + overtid
    skattetrekk per år  = brutto * skatteprosent / 100
    netto per år        = brutto - skattetrekk
    per måned           = beløp per år / 12

    overtidstimelønn    = timelønn * (1 + tillegg / 100)
    overtid av brutto   = overtid per år / brutto per år * 100
    netto per time      = netto per år / (timer per uke * 52 + overtidstimer * 12)

Forutsetninger:
    - Overtidstimer oppgis per måned (oppgaven sier ikke om det er per uke
      eller per måned), og overtiden regnes som 12 måneder i året.
    - 52 uker og 12 måneder i året. Fast skatteprosent.
    - Tar ikke hensyn til feriepenger eller bonuser.
    - Maks 50 overtidstimer i måneden (grensen etter tariffavtale for fire uker).
    - Overtidstillegget er 40 % hvis ikke annet oppgis (minimum etter loven).
    - Nøkkeltallene settes til 0 hvis nevneren er 0 (f.eks. brutto eller
      totalt antall timer er 0), for å unngå deling på null.

Oppbygging:
    Vi kunne hatt en beregn_ og en vis_, men har delt dem opp etter hva de handler om:
    beregn_lonn gjør hovedregningen, beregn_nokkeltall regner ekstra tall ut fra resultatet
    vis_ er delt i det brukeren oppga, selve lønnsresultatet og nøkkeltallene
    Da kan en del endres eller tas bort uten at resten må skrives om.
"""

from felles import skriv_overskrift, les_tall, skriv_maaned_og_aar, skriv_maaned_og_aar_overskrift, skriv_linje, formater_kr, formater_prosent, formater_tall, MAANEDER_PER_AAR, UKER_PER_AAR

def les_lonn():
    # Leser inn opplysningene lønnen regnes ut fra
    timelonn = les_tall("Skriv din timelønn: ", minimum=0, maksimum=1_000_000) #Grense for å stoppe tulle input og holde tallene innenfor tabellbredden
    timer_per_uke = les_tall("Skriv hvor mange arbeidstimer du har i uken: ",minimum=0, maksimum=168) #168 timer i en uke (24*7)
    overtids_timer = les_tall("Skriv hvor mange overtidstimer denne måneden: ", minimum=0, maksimum=50) #Med avtale kan du ha maks 50 timer overtid over 4 uker.
    overtidstillegg = les_tall("Skriv inn overtidstillegg i prosent (Enter for 40): ", minimum=0, maksimum=100, standard=40)
    skatteprosent = les_tall("Skriv hvor mange prosent du skatter: ",minimum=0, maksimum=100)

    return timelonn, timer_per_uke, overtids_timer, overtidstillegg, skatteprosent

def beregn_lonn(timelonn, timer_per_uke, overtids_timer, overtidstillegg, skatteprosent):
    # Regner ut ordinær lønn, overtid, brutto, skattetrekk og netto. Alt returneres per år
    ordinaer_aars_lonn = (timelonn * timer_per_uke) * UKER_PER_AAR
    overtid_aars_lonn = (timelonn * (1 + overtidstillegg / 100) * overtids_timer) * MAANEDER_PER_AAR
    brutto_aars_lonn = ordinaer_aars_lonn + overtid_aars_lonn
    skatte_trekk = brutto_aars_lonn * skatteprosent / 100
    netto_aars_lonn = brutto_aars_lonn - skatte_trekk

    return ordinaer_aars_lonn, overtid_aars_lonn, brutto_aars_lonn, skatte_trekk, netto_aars_lonn

def beregn_nokkeltall(timelonn, timer_per_uke, overtids_timer, overtidstillegg, overtid_aars_lonn, brutto_aars_lonn, netto_aars_lonn):
    # Regner ut overtidstimelønn, overtidens andel av brutto og netto per time
    overtid_timelonn = timelonn * (1 + overtidstillegg / 100)

    # Hvis nevneren er 0 settes svaret til 0 i stedet for å dele på null
    if brutto_aars_lonn == 0:
        overtid_andel_prosent = 0
    else:
        overtid_andel_prosent = overtid_aars_lonn / brutto_aars_lonn * 100

    timer_per_aar = timer_per_uke * UKER_PER_AAR + overtids_timer * MAANEDER_PER_AAR

    if timer_per_aar == 0:
        netto_per_time = 0
    else:
        netto_per_time = netto_aars_lonn / timer_per_aar

    return overtid_timelonn, overtid_andel_prosent, netto_per_time

def vis_oppsummering(timelonn, timer_per_uke, overtids_timer, overtidstillegg, skatteprosent):
    # Skriver ut det brukeren oppga, så det kan sjekkes mot resultatet
    skriv_linje()
    print("Du oppga:")
    print()
    print("Timelønn:", formater_kr(timelonn))
    print("Arbeidstimer per uke:", formater_tall(timer_per_uke))
    print("Overtidstimer:", formater_tall(overtids_timer))
    print("Overtidstillegg:", formater_prosent(overtidstillegg))
    print("Skatteprosent:", formater_prosent(skatteprosent))
    print()

def vis_resultat(ordinaer_aars_lonn, overtid_aars_lonn, brutto_aars_lonn, skatte_trekk, netto_aars_lonn):
    # Skriver ut lønnen per måned og per år
    skriv_maaned_og_aar_overskrift("Lønn")

    skriv_maaned_og_aar("Ordinær lønn", ordinaer_aars_lonn)
    skriv_maaned_og_aar("Overtid", overtid_aars_lonn)
    skriv_linje()
    skriv_maaned_og_aar("Lønn før skatt (Brutto)", brutto_aars_lonn)
    skriv_maaned_og_aar("Skattetrekk", skatte_trekk)
    skriv_linje()
    skriv_maaned_og_aar("Lønn etter skatt (Netto)", netto_aars_lonn)

def vis_nokkeltall(overtid_timelonn, overtid_andel_prosent, netto_per_time):
    print()
    skriv_linje()
    print("Nøkkeltall:")
    print()
    print("Overtidstimelønn:", formater_kr(overtid_timelonn))
    print("Overtid av brutto:", formater_prosent(overtid_andel_prosent))
    print("Netto per time:", formater_kr(netto_per_time))
    skriv_linje()

def kjor_lonnskalkulator():
    skriv_overskrift("Lønnskalkulator")

    timelonn, timer_per_uke, overtids_timer, overtidstillegg, skatteprosent = les_lonn()

    vis_oppsummering(timelonn, timer_per_uke, overtids_timer, overtidstillegg, skatteprosent)

    ordinaer, overtid, brutto, skatt, netto = beregn_lonn(
        timelonn, timer_per_uke, overtids_timer, overtidstillegg, skatteprosent)

    vis_resultat(ordinaer, overtid, brutto, skatt, netto)

    overtid_timelonn, overtid_andel_prosent, netto_per_time = beregn_nokkeltall(
        timelonn, timer_per_uke, overtids_timer, overtidstillegg, overtid, brutto, netto)

    vis_nokkeltall(overtid_timelonn, overtid_andel_prosent, netto_per_time)