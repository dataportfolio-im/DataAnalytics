import logging

from PYTHON_DE.loafly.models import Order
from PYTHON_DE.loafly.config import SETTINGS


def clean_price(text):
    """Turn a price written as text, like '1,250', into a number 1250.0."""
    return float(text.replace(",", "").strip())


def apply_discount(price, percent):
    """Take 'percent' off a price. apply_discount(1000, 10) -> 900.0"""
    return price - (price * percent / 100)


def build_order(raw):
    """Turn one raw order (messy text prices) into a clean Order object."""
    order = Order(raw["id"], raw["customer"])
    for name, price_text in raw["items"]:
        # EXCEPTION HANDLING: a bad price must not crash the whole run.
        try:
            price = clean_price(price_text)
        except (TypeError, AttributeError):
            logging.warning("Order %s item '%s' has no price, skipping it",
                            raw["id"], name)
            continue          # skip this item, keep going
        order.add_item(name, price)
    return order