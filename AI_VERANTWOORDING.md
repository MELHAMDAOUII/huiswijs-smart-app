
# Code leren begrijpen

Code is met AI-hulp gecontroleerd en eventueel verbeterd. 

1. **weerstation.py:** begin bij Fahrenheit. `def` definieert een functie; de parameter krijgt een waarde van de aanroeper; `return` geeft het resultaat terug. Volg daarna gevoelstemperatuur en de geneste ifs in weerrapport. Voorspel rapporten bij 0, 10 en 22 graden gevoelstemperatuur.
2. **weerstation():** `range(1, 8)` levert 1 tot en met 7. `None` betekent geen ingevoerde waarde; `0` telt wel mee. Iedere lege waarde geeft direct `return`. `totaal / dag` is pas geldig nadat alle drie de waarden voor die dag zijn ingevoerd.
3. **invoer.py:** lees eerst de basis. Volg `input`, `strip`, int/float en de while-lus. Een fout geeft een melding en `continue` begint dezelfde vraag opnieuw.
4. **controller.py:** `with open` sluit het bestand automatisch. `split()` verdeelt de regel op witruimte. De dictionary geeft de vijf velden namen. `regels[1:]` slaat de kop over. De actuatorberekening bouwt eerst alle uitvoerregels, dan opent hij de uitvoer met `w` (overschrijven).
5. **overwrite_settings:** de lijst bevat regels en iedere regel bevat vier strings. `gekozen` verwijst naar dezelfde rij in die lijst. Wijzigen van die rij verandert dus ook de lijst. `join` zet de vier velden weer samen met puntkomma's. De retourcodes hebben een afgesproken betekenis.
6. **weer_api.py:** `requests.get` haalt JSON op; `.json()` zet deze om in dictionaries. In `parameters` staan locatie, gewenste gegevens en eenheden. De API geeft wind uitdrukkelijk in m/s, passend bij de casusformule.
7. **main.py:** imports gebruiken functies uit andere bestanden. De while-lus toont opnieuw het hoofdmenu wanneer een app klaar is.


## 1. Getalconversie — invoer.py

Vóór:
```python
if geheel:
    getal = int(tekst)
else:
    getal = float(tekst.replace(",", "."))
```

Na:
```python
try:
    if geheel:
        getal = int(tekst)
    else:
        getal = float(tekst.replace(",", "."))
    if not math.isfinite(getal):
        print("Gebruik een eindig getal, geen nan of inf.")
        continue
except (ValueError, OverflowError):
    if geheel:
        print("Voer een geheel getal in, bijvoorbeeld 3. Leeg = stoppen.")
    else:
        print("Voer een getal in, bijvoorbeeld 12,5. Leeg = stoppen.")
    continue
```

Effect: `abc` bij een getal beëindigt de basis met ValueError. Na verbetering blijft dezelfde vraag actief. Leeg stopt direct en 0 blijft geldig. EOF/Ctrl+C bij de invoervraag worden als annuleren verwerkt.

### 2. Bestandsfouten — controller.py

Vóór, aan het eind van de controllerlus:
```python
voer_actie_uit(keuze, inputFile, outputFile)
```

Na:
```python
try:
    voer_actie_uit(keuze, inputFile, outputFile)
except FileNotFoundError:
    print("Bestand ontbreekt. Herstel data/input.txt of kies eerst optie 2 voor uitvoer.")
    print("Kies daarna dezelfde menu-optie opnieuw.")
except (ValueError, UnicodeError):
    print("Bestandsinhoud ongeldig. Controleer vijf velden, gehele personen en geldige getallen.")
    print("Gebruik een punt voor decimalen in TXT. Herstel het bestand en probeer opnieuw.")
except OSError:
    print("Bestand niet toegankelijk. Controleer pad en lees-/schrijfrechten en probeer opnieuw.")
```

Effect: een ontbrekend of fout bestand stopt de CLI niet. De gebruiker krijgt een gerichte herstelactie. De functies aantal_dagen en auto_bereken mogen fouten naar deze controller doorgeven; er worden geen nepresultaten zoals nul dagen bij ontbrekende invoer getoond.

### 3. Overschrijven — controller.py

Vóór:
```python
waarde = int(tekst)
```

Na:
```python
try:
    waarde = int(tekst)
except ValueError:
    print("Voer een geheel getal in; kies optie 3 opnieuw om te corrigeren.")
    return -3
```

Een wrapper overwrite_settings vangt daarnaast FileNotFoundError, OSError, UnicodeError en ValueError uit de uitvoerfile op.

### 4. API — weer_api.py

Vóór: haal_actueel_weer voert requests.get, raise_for_status, json en dictionary-toegang rechtstreeks uit.

Na: dezelfde werkende code staat in toon_actueel_weer en wordt beschermd door:
```python
def haal_actueel_weer():
    try:
        toon_actueel_weer()
    except requests.exceptions.RequestException:
        print("Weer ophalen mislukt. Controleer internet en kies optie 3 opnieuw.")
    except (ValueError, KeyError, TypeError):
        print("API gaf ongeldige of onvolledige data. Probeer optie 3 later opnieuw.")
```

Effect: timeout, HTTP-fout, verbindingsfout en foutieve JSON/data keren met een heldere melding terug naar het hoofdmenu. Er wordt geen verzonnen actuele temperatuur getoond.