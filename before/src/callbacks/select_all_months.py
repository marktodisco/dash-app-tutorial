from dash.dependencies import Input, Output
from src.data import load_transaction_data

transactions = load_transaction_data()


class SelectAllMonths:
    outputs = [Output("month-dropdown", "value"), Output("select-all-month-button-clicks", "data")]
    inputs = [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("select-all-month-button", "n_clicks"),
        Input("select-all-month-button-clicks", "data"),
    ]

    def func(
        self, years: list[int], months: list[str], n_clicks: int, previous_n_clicks: int
    ) -> tuple[list[str], int]:
        filtered_transactions = transactions.query(f"Year == {years}")
        clicked = n_clicks <= previous_n_clicks
        new_months = months if clicked else list(filtered_transactions.dropna()["Month"].unique())
        return sorted(new_months), n_clicks
