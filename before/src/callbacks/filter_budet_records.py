from typing import List

import pandas as pd
from dash.dependencies import Input, Output
from src.data import Transactions, load_transaction_data
from src.typing.aliases import BudgetRecordsAlias
from src.typing.classes import BudgetDataFrame


class FilterBudgetRecordsCallback:
    outputs = [Output("budget-pivot-table-records", "data")]
    inputs = [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("category-dropdown", "value"),
    ]

    def func(
        self, years: List[int], months: List[str], categories: List[str]
    ) -> BudgetRecordsAlias:
        transactions = self.filter_transactions(years, months, categories)
        transactions = self.create_pivot_table(transactions)
        self.drop_bad_transactions(transactions)
        return transactions.to_dict("records")  # type: ignore

    @staticmethod
    def filter_transactions(years: List[int], months: List[str], categories: List[str]):
        transactions = (
            Transactions(load_transaction_data())
            .filter(col_name="Year", values=years)
            .filter(col_name="Month", values=months)
            .filter(col_name="Category", values=categories)
        )
        transactions_df = transactions.to_data_frame().drop(columns=["Index"])
        return transactions_df

    @staticmethod
    def create_pivot_table(transactions: pd.DataFrame) -> BudgetDataFrame:
        transactions_pivot_table: BudgetDataFrame = transactions.pivot_table(  # type: ignore
            values=["Amount"],
            index=["Category"],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        ).reset_index()
        return transactions_pivot_table

    @staticmethod
    def drop_bad_transactions(transactions_pivot_table: BudgetDataFrame):
        for idx in ["Income", "Ignore"]:
            if idx in transactions_pivot_table.Category:
                transactions_pivot_table.drop(index=idx, inplace=True)
