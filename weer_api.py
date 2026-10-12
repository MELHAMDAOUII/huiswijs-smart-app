import math
import requests
from weerstation import Fahrenheit, weerrapport


def toon_actueel_weer():
    url = "https://api.open-meteo.com/v1/forecast"
    parameters = {
        "latitude": 52.0907,
        "longitude": 5.1214,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "wind_speed_unit": "ms",
        "timezone": "Europe/Amsterdam"
    }
    response = requests.get(url, params=parameters, timeout=10)
    response.raise_for_status()
    data = response.json()
    huidig = data["current"]
    temperatuur = float(huidig["temperature_2m"])
    wind = float(huidig["wind_speed_10m"])
    vochtigheid = float(huidig["relative_humidity_2m"])
    if not all((math.isfinite(temperatuur), math.isfinite(wind), math.isfinite(vochtigheid))):
        raise ValueError("Geen eindige weerwaarden")
    if wind < 0 or not 0 <= vochtigheid <= 100:
        raise ValueError("Ongeldige weerwaarden")
    print(f'Utrecht, meettijd: {huidig["time"]}')
    print(f"Temperatuur: {temperatuur:.1f}C ({Fahrenheit(temperatuur):.1f}F)")
    print(f"Wind: {wind:.1f} m/s | Luchtvochtigheid: {vochtigheid:.0f}%")
    print(weerrapport(temperatuur, wind, vochtigheid))
    print("Bron: Open-Meteo (modeldata), https://open-meteo.com/")


def haal_actueel_weer():
    try:
        toon_actueel_weer()
    except requests.exceptions.RequestException:
        print("Weer ophalen mislukt. Controleer internet en kies optie 3 opnieuw.")
    except (ValueError, KeyError, TypeError):
        print("API gaf ongeldige of onvolledige data. Probeer optie 3 later opnieuw.")
