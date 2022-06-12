import pandas as pd
from sklearn.pipeline import make_pipeline

import src
from src import transformers
from src.schema import TransactionsSchema

SETTINGS = src.config.load_settings()


def load_transaction_data() -> pd.DataFrame:
    transaction_preprocessing_pipeline = make_pipeline(
        transformers.CreateYearFromDate(),
        transformers.CreateMonthFromDate(),
    )
    raw_transactions = pd.read_csv(SETTINGS.data.path)
    transactions = transaction_preprocessing_pipeline.fit_transform(raw_transactions)
    TransactionsSchema.validate(transactions)
    return transactions
