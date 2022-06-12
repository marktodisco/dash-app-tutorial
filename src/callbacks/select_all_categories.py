import dash
import src
from dash.dependencies import Input, Output
from src.transactions import load_transaction_data

SETTINGS = src.config.load_settings()


def register(app: dash.Dash) -> None:
    @app.callback(
        Output(SETTINGS.components.category_dropdown.id, "value"),
        [
            Input(SETTINGS.components.year_dropdown.id, "value"),
            Input(SETTINGS.components.month_dropdown.id, "value"),
            Input(SETTINGS.components.category_button.id, "n_clicks"),
        ],
    )
    def _select_all_categories(year: list[int], month: list[int], _: list[int]) -> list[str]:
        categories: list[str] = list(
            load_transaction_data()
            .dropna()
            .query(f"year == {year}")
            .query(f"month == {month}")
            .loc[:, "category"]
            .unique()
        )
        return sorted(categories)
