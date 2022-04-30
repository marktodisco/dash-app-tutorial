from dash.dependencies import Input, Output
from src.data import load_transaction_data

transactions = load_transaction_data()


class UpdateCategoryDropDown:
    outputs = [Output("category-dropdown", "options")]
    inputs = [Input("year-dropdown", "value"), Input("month-dropdown", "value")]

    def func(self, year: int, month: str) -> list[dict[str, str]]:
        available_categories = list(
            transactions.dropna()
            .query(f"Year == {year}")
            .query(f"Month == {month}")["Category"]
            .unique()
        )
        options = [
            {"label": v, "value": v, "disabled": v not in available_categories}
            for v in sorted(available_categories)
        ]
        return options
