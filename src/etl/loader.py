from pathlib import Path
import pandas as pd


RAW_DATA_PATH = Path("data/raw")


FORMATTED_FILES = {
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
}


def load_excel_file(file_path):
    """
    Load a single Excel file.

    Files with title rows use header=1.
    Clean datasets use default header.
    """

    file_name = Path(file_path).name.lower()

    if file_name in FORMATTED_FILES:
        return pd.read_excel(file_path, header=1)

    return pd.read_excel(file_path)


def load_dataset(file_name):
    """
    Load dataset from data/raw folder.
    """

    file_path = RAW_DATA_PATH / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"{file_name} not found")

    return load_excel_file(file_path)


def load_all_sources():
    """
    Load all Excel files from raw directory.
    """

    datasets = {}

    for file_path in RAW_DATA_PATH.glob("*.xlsx"):
        dataset_name = file_path.stem

        datasets[dataset_name] = load_excel_file(file_path)

    return datasets