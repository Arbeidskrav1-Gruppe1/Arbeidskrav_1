"""
Felles hjelpefunksjoner og konstanter som brukes av ALLE kalkulatorene.

Begrunnelse for egen fil:
- Man slipper å skrive den samme input-valideringen 8 ganger
- Alle kalkulatorene oppfører seg likt for brukeren (samme feilmeldinger,
  samme måte å skrive tall på, samme tabelloppsett osv)
- Retter vi en feil her, er den rettet overalt

Navnsetting i hele prosjektet:
- Funksjoner og variabler: små bokstaver med understrek (snake_case)
- Konstanter: STORE_BOKSTAVER
- Vi tar ikke i bruk æ, ø og å i navn i koden. Konvertering: æ -> ae, ø -> o, å -> aa
  (f.eks belop, aar, maaned, lonn). I terminalen vises vanlig norsk språk for brukeren.
"""

# -----------------------------------------
# Konstanter som flere kalkulatorer bruker
# -----------------------------------------
MAANEDER_PER_AAR = 12
UKER_PER_AAR = 52
LINJEBREDDE = 72            # Bredden på overskrifter og linjeskille
MAKS_BELOP = 1_000_000_000  # Øvre grense for beløp, stopper "tulle input"

# -----------------------------------------
# Utskrift og formatering
# -----------------------------------------
def skriv_overskrift(tittel):
    # Skriver en tydelig overskrift med linje over og under
    print()
    print("=" * LINJEBREDDE)
    print(tittel.upper().center(LINJEBREDDE))
    print("=" * LINJEBREDDE)

def skriv_linje(tegn="-"):
    # Lager linjeskille like bred som overskriften
    print(tegn * LINJEBREDDE)

def formater_kr(belop):
    # Formatering av norsk kroneformat fra tall
    belop = round(belop, 2)
    if belop == 0:
        belop = 0.0

    tekst = f"{belop:,.2f}"          # 1,234,567.89
    tekst = tekst.replace(",", " ")  # 1 234 567.89
    tekst = tekst.replace(".", ",")  # 1 234 567,89
    return tekst + " kr"

def formater_prosent(prosent, desimaler=2):
    # Eksempel: 10.5 -> 10,50 %
    prosent = round(prosent, desimaler)
    if prosent == 0:
        prosent = 0.0
    tekst = f"{prosent:.{desimaler}f}".replace(".", ",")
    return tekst + " %"

def formater_tall(tall):
    # Formaterer til penere tall: 2.0 -> 2, 2.5 -> 2,5 (brukes i feilmeldinger)
    if tall == int(tall):
        return str(int(tall))
    return str(tall).replace(".", ",")

def skriv_maaned_og_aar(tekst, belop_aar):
    """
    Skriver en rad med beløp per måned og per år.
    Brukes av lønnskalkulatoren for at tabellen skal se lik ut.
    """
    belop_maaned = belop_aar / MAANEDER_PER_AAR
    print(f"{tekst:<30}{formater_kr(belop_maaned):>20}{formater_kr(belop_aar):>22}")

def skriv_maaned_og_aar_overskrift(tekst=""):
    # Kolonneoverskrift som hører til skriv_maaned_og_aar()
    print(f"{tekst:<30}{'Per måned':>20}{'Per år':>22}")
    skriv_linje()

# -----------------------------------------
# Robust innlesning fra brukeren
# -----------------------------------------
def tekst_til_tall(tekst):
    """
    Gjør om det brukeren skrev til et desimaltall (float).
    Godtar både komma og punktum, mellomrom (1 000) og "kr" / "%".
    Kaster ValueError hvis teksten ikke er et gyldig tall.
    """
    renset = tekst.strip().lower()
    for tegn in ("kr", "%", " "):
        renset = renset.replace(tegn, "")
    renset = renset.replace(",", ".")

    tall = float(renset)  # Kaster ValueError ved f.eks "abc"

    # Avviser spesialverdiene NaN og uendelig (inf)
    if tall != tall or tall == float("inf") or tall == float("-inf"):
        raise ValueError("Ugyldig tall")
    return tall

def les_tall(ledetekst, minimum=None, maksimum=None, standard=None):
    """
    Spør brukeren om et tall helt til svaret er gyldig.

    minimum / maksimum: grenser tallet må ligge innenfor
    standard:           verdi som brukes hvis brukeren bare trykker Enter
    """
    while True:
        tekst = input(ledetekst)

        if tekst.strip() == "" and standard is not None:
            return standard

        try:
            tall = tekst_til_tall(tekst)
        except ValueError:
            print(" Ugyldig tall. Prøv igjen (f.eks. 2500 eller 2500,50).")
            continue

        if minimum is not None and tall < minimum:
            print(f" Tallet kan ikke være mindre enn {formater_tall(minimum)}.")
            continue
        if maksimum is not None and tall > maksimum:
            print(f" Tallet kan ikke være større enn {formater_tall(maksimum)}.")
            continue

        return tall

def les_heltall(ledetekst, minimum=None, maksimum=None, standard=None):
    # Fungerer på samme måte som les_tall(), men krever et helt tall (f.eks. antall år)
    while True:
        tall = les_tall(ledetekst, minimum, maksimum, standard)
        if tall == int(tall):
            return int(tall)
        print(" Du må skrive et helt tall (uten desimaler).")

def les_ja_nei(ledetekst):
    # Returnerer True for ja og False for nei
    while True:
        svar = input(ledetekst).strip().lower()
        if svar in ("j", "ja", "y", "yes"):
            return True
        if svar in ("n", "nei", "no"):
            return False
        print(" Svar med j (ja) eller n (nei).")

def les_valg(ledetekst, gyldig_valg):
    # Spør til brukeren skriver ett av valgene i listen gyldig_valg
    while True:
        svar = input(ledetekst).strip()
        if svar in gyldig_valg:
            return svar
        print(f" Ugyldig valg. Velg en av: {', '.join(gyldig_valg)}")

def les_tekst(ledetekst, standard=""):
    # Leser inn tekst. Tomt svar gir standardverdien
    svar = input(ledetekst).strip()
    if svar == "":
        return standard
    return svar

def vent_paa_enter():
    # Pauser slik at brukeren rekker å lese resultatene før menyen vises
    input("\nTrykk Enter for å gå tilbake til menyen...")
