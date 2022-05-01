import datetime as dt

import pandas as pd
import pandera as pa
from sklearn.base import BaseEstimator, TransformerMixin

from src.data import check_date_format

YEAR_CODE = "%Y"
MONTH_CODE = "%m"
DAY_CODE = "%d"
DATE_FMT = f"{MONTH_CODE}/{DAY_CODE}/{YEAR_CODE}"
MONTH_FMT = f"{MONTH_CODE}-%b"


class DateColumnSchema(pa.SchemaModel):
    Date: pa.typing.Series[str]

    @pa.check("Date", name="date_format")
    def check_date_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[bool]:
        return check_date_format(s, DATE_FMT)


class YearColumnSchema(pa.SchemaModel):
    Year: pa.typing.Series[str]

    @pa.check("Year", name="year_format")
    def check_year_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, YEAR_CODE)


class MonthColumnSchema(pa.SchemaModel):
    Month: pa.typing.Series[str]

    @pa.check("Month", name="month_format")
    def check_month_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, MONTH_FMT)


class CreateYearFromDate(BaseEstimator, TransformerMixin):
    def fit(self, x: pd.DataFrame, y=None) -> "CreateYearFromDate":
        DateColumnSchema.validate(x)
        return self

    def transform(self, x: pd.DataFrame, y=None) -> pd.DataFrame:
        _x = x.copy()
        _x.loc[:, YearColumnSchema.Year] = (
            _x.loc[:, DateColumnSchema.Date]
            .apply(lambda d: dt.datetime.strptime(d, DATE_FMT))
            .apply(lambda d: dt.datetime.strftime(d, YEAR_CODE))
        )
        return _x


class CreateMonthFromDate(BaseEstimator, TransformerMixin):
    def fit(self, x: pd.DataFrame, y=None) -> "CreateMonthFromDate":
        DateColumnSchema.validate(x)
        return self

    def transform(self, x: pd.DataFrame, y=None) -> pd.DataFrame:
        _x = x.copy()
        _x.loc[:, MonthColumnSchema.Month] = (
            _x.loc[:, DateColumnSchema.Date]
            .apply(lambda d: dt.datetime.strptime(d, DATE_FMT))
            .apply(lambda d: dt.datetime.strftime(d, MONTH_FMT))
        )
        return _x
