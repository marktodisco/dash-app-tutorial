from typing import Any

from dash.dependencies import Input, Output
from src.data import load_transaction_data

transactions = load_transaction_data()


class UpdateYearDropdown:
    outputs = [Output("year-dropdown", "options")]
    inputs = [Input("year-dropdown", "value")]

    def func(self, *_: list[Any]) -> list[dict[str, str]]:
        available_years = transactions.dropna()["Year"].unique()
        options = [{"label": v, "value": v} for v in sorted(available_years, reverse=True)]
        return options
