from datetime import datetime
from typing import List, Dict, Union

from src.data import load_transaction_data

import pandas as pd


def get_year_options() -> List[Dict[str, str]]:
    transactions = load_transaction_data()
    return [{"label": i, "value": i} for i in transactions["Year"].unique()]


def get_month_options() -> List[Dict[str, str]]:
    transactions = load_transaction_data()
    return [{"label": i, "value": i} for i in transactions["Month"].unique()]


def get_category_options() -> List[Dict[str, str]]:
    categories = get_category_values()
    base_options = [{"label": i, "value": i} for i in categories]
    filtered_options = filter(lambda option: not pd.isna(option["label"]), base_options)
    final_options = sorted(filtered_options, key=lambda x: x["label"])
    return final_options


def get_category_values() -> List[str]:
    transactions = load_transaction_data()
    categories = transactions["Category"].unique()
    return sorted(filter(lambda category: not pd.isna(category), categories))


def get_year_values() -> List[Union[str, int]]:
    return [datetime.now().year]


def get_month_values() -> List[Union[str, int]]:
    return [datetime.now().strftime("%m-%b")]
