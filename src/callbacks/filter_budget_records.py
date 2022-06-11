from typing import Any

import dash
import pandas as pd
from dash.dependencies import Input, Output
from src.schema import TransactionsSchema
from src.transactions import load_transaction_data


def register(app: dash.Dash) -> None:
    @app.callback(
        Output("budget-pivot-table-records", "data"),
        [
            Input("year-dropdown", "value"),
            Input("month-dropdown", "value"),
            Input("category-dropdown", "value"),
        ],
    )
    def _filter_budget_records(
        years: list[int], months: list[str], categories: list[str]
    ) -> list[dict[str, Any]]:
        transactions = load_transaction_data()
        year_mask = transactions.isin(years).loc[:, TransactionsSchema.Year]
        month_mask = transactions.isin(months).loc[:, TransactionsSchema.Month]
        category_mask = transactions.isin(categories).loc[:, TransactionsSchema.Category]
        row_mask = year_mask & month_mask & category_mask
        filtered_transactions: pd.DataFrame = transactions.loc[row_mask, :]

        transactions_pivot_table = filtered_transactions.pivot_table(
            values=[TransactionsSchema.Amount],
            index=[TransactionsSchema.Category],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        ).reset_index()

        # fmt: off
        keep_rows_mask = ~(
            transactions_pivot_table
            .isin(["Income", "Ignore"])
            .loc[:, TransactionsSchema.Category]
        )
        # fmt: on
        return transactions_pivot_table.loc[keep_rows_mask, :].to_dict(orient="records")
