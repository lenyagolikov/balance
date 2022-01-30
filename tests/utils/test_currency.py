from decimal import Decimal

from app.utils import currency


def test_convert_to_EUR():
    amount = Decimal("100")
    convert = currency.convert_to_EUR(amount)
    assert amount > convert
    assert isinstance(convert, Decimal)


def test_convert_to_USD():
    amount = Decimal("100")
    convert = currency.convert_to_USD(amount)
    assert amount > convert
    assert isinstance(convert, Decimal)
