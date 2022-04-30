from dash.dependencies import Input, Output
from src.data import load_transaction_data

transactions = load_transaction_data()


class SelectAllCategories:
    outputs = [Output("category-dropdown", "value")]
    inputs = [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("select-all-category-button", "n_clicks"),
    ]

    def func(self, year: list[int], month: list[int], _: list[int]) -> list[str]:
        return list(
            transactions.dropna()
            .query(f"Year == {year}")
            .query(f"Month == {month}")["Category"]
            .unique()
        )
