from pandas import read_csv


def load_csv(fileName):
    return read_csv(fileName)


def get_string(value):
    return str(value) if "nan" != str(value) else ""
