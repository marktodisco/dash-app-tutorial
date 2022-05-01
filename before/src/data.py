import datetime as dt
from typing import Any, List, Union

import pandas as pd
import pandera as pa


def check_date_format(s: pa.typing.Series[str], fmt: str) -> pa.typing.Series[bool]:
    checks = [True if dt.datetime.strptime(_, fmt) else False for _ in s]
    return pa.typing.Series(checks, dtype=bool)


def load_transaction_data() -> pd.DataFrame:
    transactions_path = "./data/transactions-cleaned-labeled.csv"
    data = pd.read_csv(transactions_path)
    return data


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
