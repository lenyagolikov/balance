from decimal import Decimal

import requests

from app.core.config import settings


URL = "http://api.exchangeratesapi.io/v1/"


def get_unit_euro() -> dict[str, float]:
    resp = requests.get(
        f"{URL}latest?access_key={settings.EXCHANGE_RATES_API_TOKEN}&symbols=RUB"
    )
    return resp.json()["rates"]


def convert_to_USD(amount: Decimal) -> Decimal:
    resp = requests.get(
        f"{URL}latest?access_key={settings.EXCHANGE_RATES_API_TOKEN}&symbols=USD"
    )
    unit_usd = Decimal(resp.json()["rates"]["USD"])
    unit_euro = convert_to_EUR(amount)
    return unit_usd * unit_euro


def convert_to_EUR(amount: Decimal) -> Decimal:
    unit_euro = Decimal(get_unit_euro()["RUB"])
    return amount / unit_euro
