from invoer import lees_getal


def Fahrenheit(temp_celcius):
    return 32 + 1.8 * temp_celcius


def gevoelstemperatuur(temp_celcius, windsnelheid, luchtvochtigheid):
    return temp_celcius - luchtvochtigheid / 100 * windsnelheid


def weerrapport(temp_celcius, windsnelheid, luchtvochtigheid):
    gevoel = gevoelstemperatuur(temp_celcius, windsnelheid, luchtvochtigheid)
    if gevoel < 0:
        if windsnelheid > 10:
            return "Het is heel koud en het stormt! Verwarming helemaal aan!"
        return "Het is behoorlijk koud! Verwarming aan op de benedenverdieping!"
    elif gevoel < 10:
        if windsnelheid > 12:
            return "Het is best koud en het waait; verwarming aan en roosters dicht!"
        return "Het is een beetje koud, elektrische kachel op de benedenverdieping aan!"
    elif gevoel < 22:
        return "Heerlijk weer, niet te koud of te warm."
    return "Warm! Airco aan!"


def weerstation():
    print("Weerstation: maximaal 7 dagen. Leeg bij elke vraag = direct stoppen.")
    totaal = 0
    for dag in range(1, 8):
        temperatuur = lees_getal(f"Dag {dag}, temperatuur [C]: ")
        if temperatuur is None:
            print("bye")
            return
        wind = lees_getal(f"Dag {dag}, windsnelheid [m/s]: ", minimum=0)
        if wind is None:
            print("bye")
            return
        vochtigheid = lees_getal(f"Dag {dag}, vochtigheid [%]: ", True, 0, 100)
        if vochtigheid is None:
            print("bye")
            return
        totaal = totaal + temperatuur
        print(f"Het is {temperatuur:.1f}C ({Fahrenheit(temperatuur):.1f}F)")
        print(weerrapport(temperatuur, wind, vochtigheid))
        print(f"Gem. temp tot nu toe is {totaal / dag:.1f}")
        print("======================================")
    print("Alle 7 dagen zijn ingevoerd.")
