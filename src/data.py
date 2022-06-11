import datetime as dt

import pandera as pa


def check_date_format(s: pa.typing.Series[str], fmt: str) -> pa.typing.Series[bool]:
    checks = [True if dt.datetime.strptime(_, fmt) else False for _ in s]
    return pa.typing.Series(checks, dtype=bool)
