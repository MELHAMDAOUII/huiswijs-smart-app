import math
from invoer import lees_tekst


def lees_dagen(inputFile):
    with open(inputFile, "r", encoding="utf-8") as bestand:
        regels = bestand.readlines()
    if not regels or regels[0].split() != ["date", "numPeople", "tempSetpoint", "tempOutside", "precip"]:
        raise ValueError("De eerste regel moet zijn: date numPeople tempSetpoint tempOutside precip")
    dagen = []

    for regel in regels[1:]:
        if regel.strip() != "":
            velden = regel.split()
            if len(velden) != 5:
                raise ValueError("Elke dataregel moet precies vijf velden hebben.")
            dag = {
                "datum": velden[0],
                "personen": int(velden[1]),
                "setpoint": float(velden[2]),
                "buiten": float(velden[3]),
                "neerslag": float(velden[4])
            }
            if dag["personen"] < 0 or dag["neerslag"] < 0:
                raise ValueError("Personen en neerslag mogen niet negatief zijn.")
            for naam in ("setpoint", "buiten", "neerslag"):
                if not math.isfinite(dag[naam]):
                    raise ValueError("Temperaturen en neerslag moeten eindige getallen zijn.")
            for eerdere_dag in dagen:
                if eerdere_dag["datum"] == dag["datum"]:
                    raise ValueError("Een datum mag slechts eenmaal voorkomen.")
            dagen.append(dag)
    return dagen


def aantal_dagen(inputFile):
    return len(lees_dagen(inputFile))


def auto_bereken(inputFile, outputFile):
    dagen = lees_dagen(inputFile)
    uitvoer = []
    for dag in dagen:
        verschil = dag["setpoint"] - dag["buiten"]
        if verschil >= 20:
            cv = 100
        elif verschil >= 10:
            cv = 50
        else:
            cv = 0
        ventilatie = min(dag["personen"] + 1, 4)
        bewatering = dag["neerslag"] < 3
        uitvoer.append(f'{dag["datum"]};{cv};{ventilatie};{bewatering}\n')
    with open(outputFile, "w", encoding="utf-8") as bestand:
        bestand.writelines(uitvoer)



def lees_actuatoren(outputFile):
    with open(outputFile, "r", encoding="utf-8") as bestand:
        regels = bestand.readlines()
    actuatoren = []
    for regel in regels:
        if regel.strip() != "":
            rij = regel.strip().split(";")
            if len(rij) != 4:
                raise ValueError("Uitvoerregel moet datum;CV;ventilatie;bewatering bevatten.")
            if not 0 <= int(rij[1]) <= 100 or not 0 <= int(rij[2]) <= 4:
                raise ValueError("Ongeldige actuatorstand in uitvoerbestand.")
            if rij[3] not in ("True", "False"):
                raise ValueError("Bewatering in uitvoer moet True of False zijn.")
            for bestaande in actuatoren:
                if bestaande[0] == rij[0]:
                    raise ValueError("Dubbele datum in uitvoerbestand.")
            actuatoren.append(rij)
    return actuatoren


def wijzig_instellingen(outputFile):
    actuatoren = lees_actuatoren(outputFile)
    datum = lees_tekst("Datum (dd-mm-jjjj): ")
    gekozen = None
    for rij in actuatoren:
        if rij[0] == datum:
            gekozen = rij
            break
    if gekozen is None:
        return -1
    systeem = lees_tekst("Systeem: 1 CV, 2 ventilatie, 3 bewatering: ")
    if systeem not in ("1", "2", "3"):
        return -3
    tekst = lees_tekst("Nieuwe waarde (geheel getal): ")
    if tekst == "":
        return -3
    try:
        waarde = int(tekst)
    except ValueError:
        print("Voer een geheel getal in; kies optie 3 opnieuw om te corrigeren.")
        return -3
    if systeem == "1" and not 0 <= waarde <= 100:
        return -3
    if systeem == "2" and not 0 <= waarde <= 4:
        return -3
    if systeem == "3" and waarde not in (0, 1):
        return -3
    if systeem == "3":
        gekozen[3] = str(waarde == 1)
    else:
        gekozen[int(systeem)] = str(waarde)
    with open(outputFile, "w", encoding="utf-8") as bestand:
        for rij in actuatoren:
            bestand.write(";".join(rij) + "\n")
    return 0



def overwrite_settings(outputFile):
    try:
        return wijzig_instellingen(outputFile)
    except FileNotFoundError:
        print("Uitvoerbestand ontbreekt. Kies eerst optie 2 of herstel data/output.txt.")
        return -3
    except (OSError, UnicodeError, ValueError):
        print("Uitvoerbestand niet bruikbaar. Controleer rechten en formaat; kies optie 2 om opnieuw te berekenen.")
        return -3

def voer_actie_uit(keuze, inputFile, outputFile):
    if keuze == "1":
        print(f"Aantal dagen: {aantal_dagen(inputFile)}")
    elif keuze == "2":
        auto_bereken(inputFile, outputFile)
        print(f"Berekeningen opgeslagen in {outputFile}.")
    elif keuze == "3":
        code = overwrite_settings(outputFile)
        if code == 0:
            print("Waarde direct opgeslagen. Retourcode: 0.")
        elif code == -1:
            print("Datum niet gevonden. Probeer optie 3 opnieuw. Retourcode: -1.")
        else:
            print("Ongeldig systeem of waarde. Probeer optie 3 opnieuw. Retourcode: -3.")


def smart_app_controller():
    inputFile = "data/input.txt"
    outputFile = "data/output.txt"
    while True:
        print("\nSmart App Controller")
        print(f"Invoer: {inputFile} | Uitvoer: {outputFile}")
        print("1. Aantal dagen\n2. Autobereken\n3. Overschrijf\n4. Terug")
        keuze = lees_tekst("Keuze: ")
        if keuze == "4" or keuze == "":
            return
        if keuze not in ("1", "2", "3"):
            print("Kies 1, 2, 3 of 4.")
            continue
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
