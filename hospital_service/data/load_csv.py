import pandas as pd


def load_csv(fileName):
    return pd.read_csv(fileName)


def get_string(value):
    return str(value) if "nan" != str(value) else ""
