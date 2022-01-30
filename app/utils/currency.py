from decimal import Decimal

from forex_python.converter import CurrencyRates

api = CurrencyRates()


def convert_to_EUR(amount: Decimal) -> Decimal:
    return api.convert("RUB", "EUR", amount)


def convert_to_USD(amount: Decimal) -> Decimal:
    return api.convert("RUB", "USD", amount)
