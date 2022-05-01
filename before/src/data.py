from datetime import datetime
from typing import Any, List, Tuple, Union

import pandas as pd
from omegaconf import OmegaConf

from src.typing.classes import BudgetDataFrame


def load_transaction_data() -> BudgetDataFrame:
    transactions_path = "./data/transactions-cleaned-labeled.csv"
    data: BudgetDataFrame = pd.read_csv(transactions_path)  # type: ignore
    return data


def load_budget_data() -> BudgetDataFrame:
    config = OmegaConf.load("./config/budget/default.yaml")
    data = [{"Category": c, "Amount": a} for c, a in config.items()]
    df: BudgetDataFrame = pd.DataFrame(data)  # type: ignore
    return df


class Transactions:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def filter(self, col_name: str, values: Union[List[Any], Any]) -> "Transactions":
        assert col_name in self.df.columns, "col_name not in columns"

        if not isinstance(values, list):
            values = [values]
        if len(values) == 0:
            values = self.df[col_name].unique()

        mask = self.df[col_name].isin(values)  # type: ignore
        transactions = self.df.loc[mask] if len(mask) > 0 else self.df

        return Transactions(transactions)

    def to_data_frame(self) -> pd.DataFrame:
        return self.df

    def __str__(self) -> str:
        return str(self.df)


def filter_by_year_and_month(data: pd.DataFrame, year: int, month: str) -> pd.DataFrame:
    return data.query(  # type: ignore
        f"Year == {year}"
        f" & Month == '{month}'"
        " & Category != 'Ignore'"
        " & Category != 'Income'"
    )


def get_budget_table() -> pd.DataFrame:
    budget, expense, variance = load_budget_transactions_variance()
    table = create_pivot_table(budget, expense, variance)
    table["Category"] = table.index  # type: ignore
    table = table[["Category", "Planned", "Expense", "Variance"]]
    return table


def load_budget_transactions_variance(
    year: int = datetime.now().year, month: str = datetime.now().strftime("%m-%b")
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    budget = load_transaction_data().rename({"Monthly": "Planned"}, axis=1)
    budget = budget.set_index(budget["Category"]).drop(columns="Category")

    transactions = load_budget_data().rename(columns={"Amount": "Expense"})
    transactions = filter_by_year_and_month(transactions, year, month)

    expense = transactions.pivot_table(index="Category", values="Expense", aggfunc="sum")
    expense = (
        pd.concat((budget["Planned"], expense["Expense"]), axis=1).drop(columns="Planned").fillna(0)
    )

    variance = pd.DataFrame(budget["Planned"] + expense["Expense"], columns=["Variance"]).fillna(0)
    variance = pd.DataFrame(variance, columns=["Variance"])

    return budget, expense, variance


def create_pivot_table(
    budget: pd.DataFrame, expense: pd.DataFrame, variance: pd.DataFrame
) -> pd.DataFrame:
    table = pd.concat((budget[["Planned"]], expense, variance), axis=1)
    table.sort_values("Variance", inplace=True)
    totals = pd.DataFrame(table.sum(), columns=["Total"]).T
    table = pd.concat((table, totals), axis=0)
    return table


def preprocess_budget_data(df: pd.DataFrame) -> pd.DataFrame:
    budget_: pd.DataFrame = df.copy(deep=True)
    budget_ = budget_.query("Expense < 0")
    budget_ = budget_[budget_.index != "Total"]
    budget_["Expense"] *= -1
    budget_.sort_values("Expense", ascending=False, inplace=True)
    budget_["Percentage"] = (budget_["Expense"] / budget_["Expense"].sum()).map(
        lambda x: f"{x * 100:.1f}%"
    )
    budget_["ExpenseFormatted"] = budget_["Expense"].map(lambda x: f"${x:,.2f}")
    return budget_


def filter_transactions(
    transactions: pd.DataFrame, col_name: str, values: List[Any]
) -> pd.DataFrame:
    assert col_name in transactions.columns, "col_name not in columns"

    if not isinstance(values, list):
        values = [values]
    if len(values) == 0:
        values = list(transactions[col_name].unique())

    mask = transactions[col_name].isin(values)
    transactions = transactions.loc[mask] if len(mask) > 0 else transactions
    return transactions
