from datetime import datetime

from dash import html

__all__ = ["pivot_table"]

from dash_pivottable import PivotTable
from src.app_utils import generate_random_id
from src.data import load_transaction_data


def get_pivot_table() -> PivotTable:
    transactions = load_transaction_data()

    years = sorted(transactions["Year"].unique())
    months = sorted(transactions["Month"].unique())

    now = datetime.now()
    current_year = now.year
    current_month = now.strftime("%m-%b")

    year_filter = {str(year): False for year in years if year != current_year}
    month_filter = {str(month): False for month in months if month != current_month}

    return PivotTable(
        id=generate_random_id(),
        data=transactions.to_dict("records"),
        rows=["Category"],
        cols=["Year", "Month"],
        vals=["Amount"],
        rendererName="table",
        aggregatorName="Sum",
        valueFilter={"Year": year_filter, "Month": month_filter},
    )


pivot_table = html.Div(id="div-pivot-table", children=get_pivot_table())
