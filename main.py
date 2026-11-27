"""
Startpunktet for programmet. Viser hovedmenyen i terminalen og starter kalkulatoren
brukeren velger.
 
For å kjøre applikasjonen i VS Code: Åpne filen og trykk "Run Python File",
eller skriv i terminalen: python main.py
 
Alle kalkulatorene har hver sin fil og har en "kjor_..."-funksjon
som main.py henter. Hver kalkulator har samme mønster:
    1. les input -> 2. beregn -> 3. vis resultat
"""
 
from felles import skriv_overskrift, les_valg, vent_paa_enter
from moms import kjor_momskalkulator
from veksel import kjor_vekselautomat
from inflasjon import kjor_inflasjonskalkulator
from sparing import kjor_sparekalkulator
from lonn import kjor_lonnskalkulator
from budsjett import kjor_budsjett
from skatt import kjor_skattekalkulator
from pensjon import kjor_pensjonskalkulator
 
# Menyen fungerer som et dictionary: menyvalg -> (navn som vises, funksjon som kjøres)
# Bakgrunnen for denne metoden mot if/else-kjede er at det er enklere å legge til flere
# kalkulatorer senere, da det bare trengs en linje til her.
MENY = {
    "1": ("Momskalkulator", kjor_momskalkulator),
    "2": ("Vekselautomat", kjor_vekselautomat),
    "3": ("Inflasjonskalkulator", kjor_inflasjonskalkulator),
    "4": ("Sparekalkulator", kjor_sparekalkulator),
    "5": ("Lønnskalkulator", kjor_lonnskalkulator),
    "6": ("Budsjett og personlig økonomi", kjor_budsjett),
    "7": ("Skattekalkulator", kjor_skattekalkulator),
    "8": ("Pensjon og livslønn", kjor_pensjonskalkulator),
}
VALG_AVSLUTT = "9"
 
 
def vis_meny():
    # Skriver ut hovedmenyen
    skriv_overskrift("Finanskalkulator")
    print("Velg hva du vil utføre ved å taste inn et av tallene nedenfor")
    for nummer in MENY:
        navn = MENY[nummer][0]
        print(f"{nummer}: {navn}")
    print(f"{VALG_AVSLUTT}: Avslutt")
 
 
def main():
    # Hovedløkka: vis meny, kjør valgt kalkulator, gjenta til Avslutt
    gyldige_valg = list(MENY.keys()) + [VALG_AVSLUTT]
 
    while True:
        vis_meny()
        valg = les_valg("\nDitt valg: ", gyldige_valg)
 
        if valg == VALG_AVSLUTT:
            print("\nTakk for nå!")
            break
 
        navn, kalkulator_funksjon = MENY[valg]
        try:
            kalkulator_funksjon()
        except KeyboardInterrupt:
            # Ctrl + C midt i en utregning sender brukeren tilbake til menyen
            # i stedet for å krasje hele programmet.
            print(f"\n {navn} ble avbrutt.")
        vent_paa_enter()
 
 
# Kjører bare når main.py startes direkte
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgrammet avsluttes.")
