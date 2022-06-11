import dash
from dash.dependencies import Input, Output
from src.transactions import load_transaction_data


def register(app: dash.Dash) -> None:
    @app.callback(
        [Output("month-dropdown", "value"), Output("select-all-month-button-clicks", "data")],
        [
            Input("year-dropdown", "value"),
            Input("month-dropdown", "value"),
            Input("select-all-month-button", "n_clicks"),
            Input("select-all-month-button-clicks", "data"),
        ],
    )
    def _select_all_months(
        years: list[int], months: list[str], n_clicks: int, previous_n_clicks: int
    ) -> tuple[list[str], int]:
        filtered_transactions = load_transaction_data().query(f"Year == {years}")
        clicked = n_clicks <= previous_n_clicks
        new_months = months if clicked else list(filtered_transactions.dropna()["Month"].unique())
        return sorted(new_months), n_clicks
