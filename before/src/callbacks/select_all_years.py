import dash
from dash.dependencies import Input, Output
from src.transactions import load_transaction_data


def register(app: dash.Dash) -> None:
    @app.callback(
        [Output("year-dropdown", "value"), Output("select-all-year-button-clicks", "data")],
        [
            Input("year-dropdown", "value"),
            Input("select-all-year-button", "n_clicks"),
            Input("select-all-year-button-clicks", "data"),
        ],
    )
    def select_all_years(
        years: list[str], n_clicks: int, previous_n_clicks: int
    ) -> tuple[list[str], int]:
        clicked = n_clicks <= previous_n_clicks
        new_years = years if clicked else list(load_transaction_data().dropna()["Year"].unique())
        return sorted(new_years), n_clicks
