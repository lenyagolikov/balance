from decimal import Decimal

import requests

from app.core.config import settings


URL = "http://api.exchangeratesapi.io/v1/"


def unit_euro():
    resp = requests.get(
        f"{URL}latest?access_key={settings.EXCHANGE_RATES_API_TOKEN}&symbols=RUB"
    )
    return resp.json()["rates"]["RUB"]


def transfer_to_USD(value: Decimal) -> Decimal:
    resp = requests.get(
        f"{URL}latest?access_key={settings.EXCHANGE_RATES_API_TOKEN}&symbols=USD"
    )
    unit_usd = Decimal(resp.json()["rates"]["USD"])
    unit_euro = transfer_to_EUR(value)
    return unit_usd * unit_euro


def transfer_to_EUR(value: Decimal) -> Decimal:
    return value / Decimal(unit_euro())
