from dash.dependencies import Input, Output
from src.data import load_transaction_data

transactions = load_transaction_data()


class UpdateMonthDropDown:
    outputs = [Output("month-dropdown", "options")]
    inputs = [Input("year-dropdown", "value")]

    def func(self, years: list[list[int]]) -> list[dict[str, str]]:
        available_months = list(transactions.dropna().query(f"Year == {years}")["Month"].unique())
        options = [
            {"label": m, "value": m, "disabled": m not in available_months}
            for m in sorted(available_months)
        ]
        return options
