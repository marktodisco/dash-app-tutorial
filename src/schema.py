import pandera as pa

from src.data import check_date_format

YEAR_CODE = "%Y"
MONTH_CODE = "%m"
DAY_CODE = "%d"
DATE_FMT = f"{MONTH_CODE}/{DAY_CODE}/{YEAR_CODE}"
MONTH_FMT = f"{MONTH_CODE}-%b"


class RawTransactionsSchema(pa.SchemaModel):
    Date: pa.typing.Series[str]
    Amount: pa.typing.Series[float]
    Category: pa.typing.Series[str] = pa.Field(nullable=True)


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


class TransactionsSchema(pa.SchemaModel):
    Date: pa.typing.Series[str]
    Amount: pa.typing.Series[float]
    Category: pa.typing.Series[str] = pa.Field(nullable=True)
    Year: pa.typing.Series[str]
    Month: pa.typing.Series[str]

    @pa.check("Date")
    def check_date(cls, s: pa.typing.Series[str]) -> pa.typing.Series[bool]:
        return check_date_format(s, "%m/%d/%Y")

    @pa.check("Year", name="year_format")
    def check_year_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, "%Y")

    @pa.check("Month", name="month_format")
    def check_month_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, "%m-%b")
