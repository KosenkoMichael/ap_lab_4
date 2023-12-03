import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_processed_df(path: str) -> pd.DataFrame:
    """Reading and processing according to the variant of data from the dataset
    Args:
      path: the path to the file for reading information
    Returns:
      Dataframe without NaN values and with the addition of the Fahrenheit temperature column
    """
    df = pd.read_csv(path, header=None)
    df.columns = ["Date",
                  "Day celsius temperature", "Day press", "Day wind dirrection", "Day wind speed",
                  "Night celsius temperature", "Night press", "Night wind dirrection", "Night wind speed"]
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
    if not ((df.isnull().sum()).eq(0).all()):
        df.dropna(inplace=True, ignore_index=True)
    df['Day fahrenheit temperature'] = 9/5 * df['Day celsius temperature'] + 32
    df['Night fahrenheit temperature'] = 9 / \
        5 * df['Night celsius temperature'] + 32
    return df