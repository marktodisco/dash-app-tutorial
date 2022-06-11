import pandas as pd
from sklearn.pipeline import make_pipeline

from src import transformers
from src.schema import TransactionsSchema


def load_transaction_data() -> pd.DataFrame:
    transaction_preprocessing_pipeline = make_pipeline(
        transformers.CreateYearFromDate(),
        transformers.CreateMonthFromDate(),
    )
    raw_transactions = pd.read_csv("./data/transactions.csv")
    transactions = transaction_preprocessing_pipeline.fit_transform(raw_transactions)
    TransactionsSchema.validate(transactions)
    return transactions
