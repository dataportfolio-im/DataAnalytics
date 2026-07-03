
import pandas as pd
from PYTHON_DE.loafly.config import SETTINGS

def fetch_todays_orders():
    """Return today's raw orders, exactly as they arrived."""
    df= pd.read_csv(SETTINGS["filepath"])
    orders = []

    for order_id in df["order_id"].unique():
        order = df[df["order_id"] == order_id]

        orders.append({
            "id": order_id,
            "customer": order["customer"].iloc[0],
            "items": list(zip(order["item_name"], order["item_price"]))
        })

    return orders