import datetime as dt

import pandas as pd
import pandera as pa
from sklearn.base import BaseEstimator, TransformerMixin

import src
from src.data import check_date_format

SETTINGS = src.config.load_settings()


class DateColumnSchema(pa.SchemaModel):
    date: pa.typing.Series[str]

    @pa.check("date", name="date_format")
    def check_date_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[bool]:
        return check_date_format(s, SETTINGS.dates.date_format)


class YearColumnSchema(pa.SchemaModel):
    year: pa.typing.Series[str]

    @pa.check("year", name="year_format")
    def check_year_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, SETTINGS.dates.year_format)


class MonthColumnSchema(pa.SchemaModel):
    month: pa.typing.Series[str]

    @pa.check("month", name="month_format")
    def check_month_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, SETTINGS.dates.month_format)


class CreateYearFromDate(BaseEstimator, TransformerMixin):
    def fit(self, x: pd.DataFrame, y=None) -> "CreateYearFromDate":
        DateColumnSchema.validate(x)
        return self

    def transform(self, x: pd.DataFrame, y=None) -> pd.DataFrame:
        _x = x.copy()
        _x.loc[:, YearColumnSchema.year] = (
            _x.loc[:, DateColumnSchema.date]
            .apply(lambda d: dt.datetime.strptime(d, SETTINGS.dates.date_format))
            .apply(lambda d: dt.datetime.strftime(d, SETTINGS.dates.year_format))
        )
        return _x


class CreateMonthFromDate(BaseEstimator, TransformerMixin):
    def fit(self, x: pd.DataFrame, y=None) -> "CreateMonthFromDate":
        DateColumnSchema.validate(x)
        return self

    def transform(self, x: pd.DataFrame, y=None) -> pd.DataFrame:
        _x = x.copy()
        _x.loc[:, MonthColumnSchema.month] = (
            _x.loc[:, DateColumnSchema.date]
            .apply(lambda d: dt.datetime.strptime(d, SETTINGS.dates.date_format))
            .apply(lambda d: dt.datetime.strftime(d, SETTINGS.dates.month_format))
        )
        return _x
