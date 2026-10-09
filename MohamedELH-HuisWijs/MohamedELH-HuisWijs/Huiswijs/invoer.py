import math


def lees_tekst(vraag):
    try:
        return input(vraag).strip()
    except EOFError:
        print("Geen invoer meer beschikbaar; deze actie stopt.")
        return ""
    except KeyboardInterrupt:
        print("\nDeze actie is gestopt.")
        return ""


def lees_getal(vraag, geheel=False, minimum=None, maximum=None):
    # Alleen deze conversie is beveiligd; de berekeningen blijven gelijk.
    while True:
        tekst = lees_tekst(vraag)
        if tekst == "":
            return None
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
        if minimum is not None and getal < minimum:
            print(f"Voer een waarde van minimaal {minimum} in.")
        elif maximum is not None and getal > maximum:
            print(f"Voer een waarde van maximaal {maximum} in.")
        else:
            return getal
