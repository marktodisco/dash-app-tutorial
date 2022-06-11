import dash
from dash.dependencies import Input, Output
from src.transactions import load_transaction_data


def register(app: dash.Dash) -> None:
    @app.callback(
        Output("category-dropdown", "value"),
        [
            Input("year-dropdown", "value"),
            Input("month-dropdown", "value"),
            Input("select-all-category-button", "n_clicks"),
        ],
    )
    def _select_all_categories(year: list[int], month: list[int], _: list[int]) -> list[str]:
        categories: list[str] = list(
            load_transaction_data()
            .dropna()
            .query(f"Year == {year}")
            .query(f"Month == {month}")
            .loc[:, "Category"]
            .unique()
        )
        return sorted(categories)
