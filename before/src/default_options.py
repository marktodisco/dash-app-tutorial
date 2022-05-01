from datetime import datetime

import pandas as pd

from src.typing.classes import BudgetDataFrame


def get_year_options(transactions: BudgetDataFrame) -> list[dict[str, str]]:
    return [{"label": i, "value": i} for i in transactions["Year"].unique()]


def get_month_options(transactions: BudgetDataFrame) -> list[dict[str, str]]:
    return [{"label": i, "value": i} for i in transactions["Month"].unique()]


def get_category_options(transactions: BudgetDataFrame) -> list[dict[str, str]]:
    categories = get_category_values(transactions)
    base_options = [{"label": i, "value": i} for i in categories]
    filtered_options = filter(lambda option: not pd.isna(option["label"]), base_options)
    final_options = sorted(filtered_options, key=lambda x: x["label"])
    return final_options


def get_category_values(transactions: BudgetDataFrame) -> list[str]:
    categories = transactions["Category"].unique()
    return sorted(filter(lambda category: not pd.isna(category), categories))


def get_year_values() -> list[str | int]:
    return [datetime.now().year]


def get_month_values() -> list[str | int]:
    return [datetime.now().strftime("%m-%b")]
