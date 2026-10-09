from invoer import lees_tekst
from weerstation import weerstation
from controller import smart_app_controller
from weer_api import haal_actueel_weer


def main():
    while True:
        print("\nWelkom bij HuisWijs - jouw weer, jouw slimme huis!")
        print("1. Weerstation\n2. Smart App Controller\n3. Actueel weer Utrecht\n4. Stoppen")
        keuze = lees_tekst("Keuze: ")
        if keuze == "1":
            weerstation()
        elif keuze == "2":
            smart_app_controller()
        elif keuze == "3":
            haal_actueel_weer()
        elif keuze == "4" or keuze == "":
            print("Tot ziens!")
            return
        else:
            print("Kies 1, 2, 3 of 4.")


if __name__ == "__main__":
    main()
