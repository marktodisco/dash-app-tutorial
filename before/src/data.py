import datetime as dt

import pandas as pd
import pandera as pa


def check_date_format(s: pa.typing.Series[str], fmt: str) -> pa.typing.Series[bool]:
    checks = [True if dt.datetime.strptime(_, fmt) else False for _ in s]
    return pa.typing.Series(checks, dtype=bool)


def load_transaction_data() -> pd.DataFrame:
    transactions_path = "./data/transactions-cleaned-labeled.csv"
    data = pd.read_csv(transactions_path)
    return data
