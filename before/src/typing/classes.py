import pandas as pd


class BudgetDataFrame(pd.DataFrame):
    Category: pd.Series
    Amount: pd.Series


class BudgetTableDataFrame(pd.DataFrame):
    Category: pd.Series
    Planned: pd.Series
    Actual: pd.Series
    Variance: pd.Series
    Percentage: pd.Series


class BudgetTableDataFrameRow(pd.Series):
    Category: str
    Planned: float
    Actual: float
    Variance: float
    Percentage: float
