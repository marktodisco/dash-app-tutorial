from datetime import datetime

import pandas as pd
import pandera as pa

from src.data import create_date_check_func

YEAR_SCHEMA = pa.DataFrameSchema(
    columns={"Year": pa.Column(str, pa.Check(create_date_check_func("%Y")))}
)
MONTH_SCHEMA = pa.DataFrameSchema(
    columns={"Month": pa.Column(str, pa.Check(create_date_check_func("%m-%b")))}
)
CATEGORY_SCHEMA = pa.DataFrameSchema(columns={"Category": pa.Column(str, nullable=True)})


def get_year_options(transactions: pd.DataFrame) -> list[dict[str, str]]:
    # YEAR_SCHEMA.validate(transactions)
    return [{"label": i, "value": i} for i in transactions["Year"].unique()]


def get_month_options(transactions: pd.DataFrame) -> list[dict[str, str]]:
    MONTH_SCHEMA.validate(transactions)
    return [{"label": i, "value": i} for i in transactions["Month"].unique()]


def get_category_options(transactions: pd.DataFrame) -> list[dict[str, str]]:
    categories = get_category_values(transactions)
    base_options = [{"label": i, "value": i} for i in categories]
    filtered_options = filter(lambda option: not pd.isna(option["label"]), base_options)
    final_options = sorted(filtered_options, key=lambda x: x["label"])
    return final_options


def get_category_values(transactions: pd.DataFrame) -> list[str]:
    CATEGORY_SCHEMA.validate(transactions)
    categories = transactions["Category"].unique()
    return sorted(filter(lambda category: not pd.isna(category), categories))


def get_year_values() -> list[str | int]:
    return [datetime.now().year]


def get_month_values() -> list[str | int]:
    return [datetime.now().strftime("%m-%b")]
