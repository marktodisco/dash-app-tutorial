import pandera as pa

from src.data import check_date_format


class TransactionsSchema(pa.SchemaModel):
    Date: pa.typing.Series[str]
    Year: pa.typing.Series
    Month: pa.typing.Series[str]
    Amount: pa.typing.Series[float]
    Label: pa.typing.Series[str]
    Account: pa.typing.Series[str]
    Description: pa.typing.Series[str]
    Category: pa.typing.Series[str] = pa.Field(nullable=True)

    @pa.check("Date", name="date_format")
    def check_date_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[bool]:
        return check_date_format(s, "%m/%d/%Y")

    # @pa.check("Year", name="year_format")
    # def check_year_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
    #     return check_date_format(s, "%Y")

    @pa.check("Month", name="month_format")
    def check_month_format(cls, s: pa.typing.Series[str]) -> pa.typing.Series[str]:
        return check_date_format(s, "%m-%b")
