# Finanskalkulator

Et terminalbasert Python-program med åtte kalkulatorer innen økonomi, finans og regnskap. Brukeren velger kalkulator fra en meny, skriver inn tallene og får resultatet presentert i terminalen.

Prosjektet er laget som gruppeoppgave i **Programmering** (Arbeidskrav 1, Del 2) ved Fagskolen Innlandet, med utgangspunkt i pensum fra Cisco Networking Academy *Python Essentials 1*.

---

## Innhold

- [Funksjoner](#funksjoner)
- [Krav](#krav)
- [Kom i gang](#kom-i-gang)
- [Prosjektstruktur](#prosjektstruktur)
- [Oppbygging og designvalg](#oppbygging-og-designvalg)
- [Navnekonvensjon](#navnekonvensjon)
- [Kalkulatorene](#kalkulatorene)
- [Eksempel på kjøring](#eksempel-på-kjøring)
- [Status](#status)
- [Gruppe](#gruppe)

---

## Funksjoner

| Meny | Kalkulator | Kort beskrivelse |
|:---:|---|---|
| 1 | Momskalkulator | Mva for én eller flere varer, med sum per momssats |
| 2 | Vekselautomat | Veksel fordelt på norske sedler og mynter |
| 3 | Inflasjonskalkulator | Prisutvikling og kjøpekraft med inflasjon som kan variere fra år til år |
| 4 | Sparekalkulator | Saldo, innskudd og renter år for år med månedlig rente |
| 5 | Lønnskalkulator | Ordinær lønn, overtid, skatt og netto per måned og år |
| 6 | Budsjett og personlig økonomi | Månedsbudsjett med andel av inntekt og forslag til sparing |
| 7 | Skattekalkulator | Skatt på lønnsinntekt etter satsene for 2026 |
| 8 | Pensjon og livslønn | Lønnsutvikling, livslønn og estimert pensjon |

**Felles for alle kalkulatorene:**

- Robust input: programmet spør på nytt helt til svaret er gyldig, i stedet for å krasje
- Godtar både `1500`, `1500,50`, `1 500` og `1500 kr`
- Beløp vises i norsk format: `1 234,56 kr`
- Ingen eksterne bibliotek, kun Python sin standard

---

## Krav

- **Python 3.6 eller nyere**
- Ingen eksterne pakker. Det er ingenting å installere med `pip`.

Sjekk hvilken versjon du har:

```bash
python --version
```

---

## Kom i gang

**1. Last ned prosjektet**

```bash
git clone <https://github.com/Arbeidskrav1-Gruppe1>
cd finanskalkulator
```

Eller last ned som zip fra GitHub (**Code → Download ZIP**) og pakk ut.

**2. Kjør programmet**

```bash
python main.py
```

**I VS Code:** Åpne mappen med **File → Open Folder**, åpne `main.py` og trykk (*Run Python File*) oppe til høyre.

> **Merk:** Programmet må alltid startes fra `main.py`. De andre filene inneholder bare funksjoner som `main.py` henter, og gjør ingenting når de kjøres alene.

---

## Prosjektstruktur

```
finanskalkulator/
├── main.py        
├── felles.py      
├── moms.py        
├── veksel.py      
├── inflasjon.py   
├── sparing.py     
├── lonn.py        
├── budsjett.py    
├── skatt.py       
├── pensjon.py     
└── README.md
```

Alle filene må ligge i samme mappe, fordi `main.py` henter kalkulatorene med `import`.

---

## Oppbygging og designvalg

### Samme mønster i alle kalkulatorene

Hver kalkulator følger de samme tre stegene:

```
1. les input  ->  2. beregn  ->  3. vis resultat
```

| Funksjon | Ansvar |
|---|---|
| `kjor_...()` | Starter kalkulatoren, leser input og binder stegene sammen. Det er denne `main.py` kaller. |
| `beregn_...()` | Gjør selve utregningen og returnerer svaret. Inneholder ingen `input()` eller `print()`. |
| `vis_resultat()` | Skriver ut resultatet. Inneholder ingen utregning. |

Når beregning og utskrift holdes adskilt, er det lett å finne feil. Blir tallet galt, ligger feilen i `beregn_...()`. Ser utskriften rar ut, ligger feilen i `vis_resultat()`.

### Felles hjelpefunksjoner (`felles.py`)

Alt kalkulatorene har felles ligger i én fil:

| Funksjon | Hva den gjør |
|---|---|
| `les_tall()` | Leser et tall, med valgfri minimum, maksimum og standardverdi |
| `les_heltall()` | Som `les_tall()`, men krever et helt tall |
| `les_ja_nei()` | Returnerer `True` for ja og `False` for nei |
| `les_valg()` | Spør til brukeren velger et gyldig menyvalg |
| `formater_kr()` | `1234.5` → `1 234,50 kr` |
| `formater_prosent()` | `12.5` → `12,50 %` |
| `skriv_overskrift()` | Skriver en tydelig overskrift med linje over og under |
| `vent_paa_enter()` | Pause slik at brukeren rekker å lese resultatet |

Dermed slipper vi å skrive den samme input-valideringen åtte ganger, alle kalkulatorene oppfører seg likt for brukeren, og en feil som rettes her er rettet overalt.

### Menyen er et dictionary

Menyen i `main.py` er et dictionary i stedet for en lang `if/elif`-kjede:

```python
MENY = {
    "1": ("Momskalkulator", kjor_momskalkulator),
    "2": ("Vekselautomat", kjor_vekselautomat),
    ...
}
```

Hver linje kobler et menyvalg til navnet som vises og funksjonen som kjøres. For å legge til en ny kalkulator trengs bare én ny linje.

---

## Navnekonvensjon

Hele prosjektet følger samme standard:

| Type | Stil | Eksempel |
|---|---|---|
| Funksjoner og variabler | `snake_case` | `les_tall`, `belop_ekskl` |
| Konstanter | `STORE_BOKSTAVER` | `MVA_SATSER`, `PERSONFRADRAG` |
| Prosentverdier | Slutter på `_prosent` | `sats_prosent`, `rente_prosent` |
| Kalkulatorens startfunksjon | `kjor_...` | `kjor_momskalkulator` |

Vi bruker ikke æ, ø og å i navn i koden: **æ → ae, ø → o, å → aa** (f.eks. `belop`, `aar`, `maaned`, `lonn`). Tekst som vises for brukeren skrives på vanlig norsk.

---

## Kalkulatorene

<details>
<summary><b>1. Momskalkulator</b></summary>

- **Input:** navn, beløp, om beløpet er inkl. eller ekskl. mva, og momskategori, for én eller flere varer
- **Output:** for hver vare ekskl. mva, mva-beløp og inkl. mva; samlet sum og mva-sum per sats
- **Forutsetninger:** bare satsene 25, 15, 12 og 0 %

```
inkl. mva  = ekskl. mva * (1 + sats/100)
ekskl. mva = inkl. mva / (1 + sats/100)
mva        = inkl. mva - ekskl. mva
```
</details>

<details>
<summary><b>2. Vekselautomat</b></summary>

- **Input:** pris og innbetalt beløp
- **Output:** totalt beløp tilbake og antall av hver seddel og mynt
- **Valg:** regner i hele øre (heltall) for å unngå avrundingsfeil med desimaltall. Vekselen rundes av til hele kroner, siden Norge ikke har øremynter.
</details>

<details>
<summary><b>3. Inflasjonskalkulator</b></summary>

- **Input:** beløp, antall år og inflasjon for hvert år
- **Output:** utvikling år for år, fremtidig pris, kjøpekraft i dagens kroner og samlet prisstigning
- **Forutsetninger:** inflasjonen kan variere fra år til år
</details>

<details>
<summary><b>4. Sparekalkulator</b></summary>

- **Input:** startbeløp, månedlig sparebeløp, årlig rente og antall år
- **Output:** innskutt, renter og saldo år for år; sluttsum og totalt opptjent rente
- **Forutsetninger:** fast rente, renten legges til månedlig (årsrente / 12), ingen skatt eller gebyrer
- **Valg:** renten beregnes før månedens innskudd, slik at innskuddet regnes som satt inn på slutten av måneden
</details>

<details>
<summary><b>5. Lønnskalkulator</b></summary>

- **Input:** timelønn, timer per uke, overtidstimer per uke, overtidstillegg og skatteprosent
- **Output:** ordinær lønn, overtid, brutto, skattetrekk og netto, per måned og per år
- **Forutsetninger:** fast skatteprosent, 52 uker og 12 måneder, ingen feriepenger eller bonus
- **Valg:** overtidstimer tolkes som timer *per uke*, på samme måte som ordinære timer
</details>

<details>
<summary><b>6. Budsjett og personlig økonomi</b></summary>

- **Input:** inntekt per måned etter skatt og utgifter per forhåndsdefinert kategori
- **Output:** utgifter per kategori med andel av inntekt, sum utgifter, overskudd eller underskudd per måned og år, og forslag
- **Regler for forslagene:**
  - 10–20 % av inntekten bør spares
  - største utgiftspost pekes ut, med hva et kutt på 10 % vil spare
</details>

<details>
<summary><b>7. Skattekalkulator</b></summary>

- **Input:** brutto årsinntekt og eventuelle andre fradrag
- **Output:** skatt på alminnelig inntekt (22 %), trinnskatt og trygdeavgift (7,6 %); total skatt, effektiv skattesats og netto per år og måned
- **Forutsetninger:** forenklet modell for lønnsinntekt, én person, inntektsåret 2026

| Sats (2026) | Verdi |
|---|---|
| Skatt på alminnelig inntekt | 22 % |
| Personfradrag | 114 540 kr |
| Minstefradrag | 46 %, maks 95 700 kr |
| Trygdeavgift | 7,6 % (nedre grense 99 650 kr) |
| Trinnskatt trinn 1–5 | 1,7 % / 4,0 % / 13,7 % / 16,8 % / 17,8 % |
| Innslagspunkter | 226 100 / 318 300 / 725 050 / 980 100 / 1 467 200 kr |

Satsene ligger som konstanter øverst i `skatt.py` og må oppdateres for et nytt inntektsår.
</details>

<details>
<summary><b>8. Pensjon og livslønn</b></summary>

- **Input:** startalder, pensjonsalder, startlønn, årlig lønnsvekst, pensjonssparing (% av lønn) og forventet avkastning
- **Output:** lønnsutvikling, samlet inntekt, pensjonsbeholdning ved pensjonsalder og pensjon per år og måned
- **Forutsetninger:** folketrygden (NAV) er ikke med, fast lønnsvekst og avkastning, ingen skatt, pensjonen tas ut jevnt til 85 år
</details>

---

## Eksempel på kjøring

Momskalkulatoren med to varer:

```
========================================================================
                            RESULTAT - MOMS
========================================================================
Brød (15 % mva)
  Ekskl. mva: 34,78 kr
  Mva:        5,22 kr
  Inkl. mva:  40,00 kr

Sko (25 % mva)
  Ekskl. mva: 1 000,00 kr
  Mva:        250,00 kr
  Inkl. mva:  1 250,00 kr

SAMLET SUM
  Ekskl. mva: 1 034,78 kr
  Mva:        255,22 kr
  Inkl. mva:  1 290,00 kr

MVA PER SATS
  25 %: 250,00 kr
  15 %: 5,22 kr
  12 %: 0,00 kr
  0 %: 0,00 kr
```

---

## Status

- [x] Hovedmeny (`main.py`)
- [x] Felles hjelpefunksjoner (`felles.py`)
- [x] Momskalkulator
- [x] Vekselautomat
- [ ] Inflasjonskalkulator
- [ ] Sparekalkulator
- [x] Lønnskalkulator
- [x] Budsjett og personlig økonomi
- [x] Skattekalkulator
- [x] Pensjon og livslønn

---

## Gruppe

| Navn | Rolle |
|---|---|
| *Erik Schieldrop* | *Struktur for kodebasen, main.py, felles.py, moms.py, budsjett.py og skatt.py* |
| *Sondre Ludvigsen* | *veksel.py, lonn.py og pensjon.py* |
| *Sondre Skamfer* | *inflasjon.py og spare.py* |

**Emne:** Programmering, Fagskolen Innlandet
**Oppgave:** Arbeidskrav 1, Del 2
**Levering:** 4. desember 2026

---

## Kilder

Finansdepartementet. (2025). *Skattesatser 2026*. Regjeringen. https://www.regjeringen.no/no/tema/okonomi-og-budsjett/skatter-og-avgifter/skattesatser-2026/id3121978/
