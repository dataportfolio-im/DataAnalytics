import logging

# Import only what we need, from the module it lives in.
from PYTHON_DE.loafly.extract import fetch_todays_orders
from PYTHON_DE.loafly.transform import build_order, apply_discount
from PYTHON_DE.loafly.load import save_order
from PYTHON_DE.loafly.config import SETTINGS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers =[logging.FileHandler("PYTHON_DE/logs/pipeline.log"),
                logging.StreamHandler()
    ]

)


def main():
    logging.info("Starting today's order run")
    for raw in fetch_todays_orders():                   # EXTRACT
        order = build_order(raw)                        # TRANSFORM
        subtotal = order.total()
        final = apply_discount(subtotal, SETTINGS["discount_percent"])
        logging.info("Order %s total: %s %.2f (after %d%% discount)",
                     order.order_id, SETTINGS["currency"], final,
                     SETTINGS["discount_percent"])
        save_order(order)                               # LOAD
    logging.info("Order run finished")


if __name__ == "__main__":
    main()