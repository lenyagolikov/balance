from decimal import Decimal

from app.utils import currency


def test_get_unit_euro():
    unit_euro = currency.get_unit_euro()
    assert "RUB" in unit_euro


def test_convert_to_EUR():
    amount = 100
    convert = currency.convert_to_EUR(amount)
    assert amount > convert
    assert isinstance(convert, Decimal)


def test_convert_to_USD():
    amount = 100
    convert = currency.convert_to_USD(amount)
    assert amount > convert
    assert isinstance(convert, Decimal)
