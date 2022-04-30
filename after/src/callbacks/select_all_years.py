from dash.dependencies import Input, Output
from src.data import load_transaction_data

transactions = load_transaction_data()


class SelectAllYears:
    outputs = [Output("year-dropdown", "value"), Output("select-all-year-button-clicks", "data")]
    inputs = [
        Input("year-dropdown", "value"),
        Input("select-all-year-button", "n_clicks"),
        Input("select-all-year-button-clicks", "data"),
    ]

    def func(
        self, years: list[int], n_clicks: int, previous_n_clicks: int
    ) -> tuple[list[int], int]:
        clicked = n_clicks <= previous_n_clicks
        new_years = years if clicked else list(transactions.dropna()["Year"].unique())
        return sorted(new_years), n_clicks
