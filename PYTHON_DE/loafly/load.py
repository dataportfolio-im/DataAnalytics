import os
import time
import logging

from PYTHON_DE.loafly.config import SETTINGS
from PYTHON_DE.data.starter.gateway import save_to_orders_api


def get_api_key():
    return os.getenv("LOAFLY_API_KEY", "demo-key")


def save_order(order):
    """RETRY: saving can fail (a network blip). Try a few times, then give up."""
    api_key = get_api_key()                 
    retries = SETTINGS["max_save_retries"]
    for attempt in range(1, retries + 1):
        try:  
            save_to_orders_api(order.order_id, order.total())
            logging.info(
                "Saved order %s for %s",
                order.order_id,
                order.customer
            )
            return True
        except ConnectionError:
            logging.warning(
                "Save failed for order %s (attempt %s), trying again",
                order.order_id,
                attempt
            )
            time.sleep(0.5)
    logging.error(
        "Gave up saving order %s",
        order.order_id
    )
    return False
