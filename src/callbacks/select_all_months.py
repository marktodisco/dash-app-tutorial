import dash
import src
from dash.dependencies import Input, Output
from src.transactions import load_transaction_data

SETTINGS = src.config.load_settings()


def register(app: dash.Dash) -> None:
    @app.callback(
        [
            Output(SETTINGS.components.month_dropdown.id, "value"),
            Output(SETTINGS.components.month_button_clicks.id, "data"),
        ],
        [
            Input(SETTINGS.components.year_dropdown.id, "value"),
            Input(SETTINGS.components.month_dropdown.id, "value"),
            Input(SETTINGS.components.month_button.id, "n_clicks"),
            Input(SETTINGS.components.month_button_clicks.id, "data"),
        ],
    )
    def _select_all_months(
        years: list[int], months: list[str], n_clicks: int, previous_n_clicks: int
    ) -> tuple[list[str], int]:
        filtered_transactions = load_transaction_data().query(
            f"{src.schema.YearColumnSchema.year} == {years}"
        )
        clicked = n_clicks <= previous_n_clicks
        new_months = (
            months
            if clicked
            else list(filtered_transactions[src.schema.MonthColumnSchema.month].unique())
        )
        return sorted(new_months), n_clicks
