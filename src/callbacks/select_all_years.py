import dash
import src
from dash.dependencies import Input, Output
from src.transactions import load_transaction_data

SETTINGS = src.config.load_settings()


def register(app: dash.Dash) -> None:
    @app.callback(
        [
            Output(SETTINGS.components.year_dropdown.id, "value"),
            Output(SETTINGS.components.year_button_clicks.id, "data"),
        ],
        [
            Input(SETTINGS.components.year_dropdown.id, "value"),
            Input(SETTINGS.components.year_button.id, "n_clicks"),
            Input(SETTINGS.components.year_button_clicks.id, "data"),
        ],
    )
    def select_all_years(
        years: list[str], n_clicks: int, previous_n_clicks: int
    ) -> tuple[list[str], int]:
        clicked = n_clicks <= previous_n_clicks
        new_years = years if clicked else list(load_transaction_data().dropna()["year"].unique())
        return sorted(new_years), n_clicks
