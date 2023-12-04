import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_processed_df(path: str) -> pd.DataFrame:
    """read csv file and create dataframe
    Args:
      path: path to dataset
    Returns:
      Dataframe without NaN values and with the addition of the Fahrenheit temperature column
    """
    df = pd.read_csv(path, header=None)
    df.columns = ["Date",
                  "Day celsius temperature", "Day press", "Day wind dirrection", "Day wind speed",
                  "Night celsius temperature", "Night press", "Night wind dirrection", "Night wind speed"]
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    if not ((df.isnull().sum()).eq(0).all()):
        df.dropna(inplace=True, ignore_index=True)
    df['Day fahrenheit temperature'] = 9/5 * df['Day celsius temperature'] + 32
    df['Night fahrenheit temperature'] = 9 / \
        5 * df['Night celsius temperature'] + 32
    return df


# | None:
def get_statistical_info(df: pd.DataFrame, parametr: str) -> pd.Series:
    """Getting statistical information
    Args:
      df: Dataframe with original values
      parametr: column for statistic
    Returns:
      A series containing a statistical info
    """
    if parametr in df.columns:
        return df[parametr].describe()


def celsius_temp_filtration(df: pd.DataFrame, celsius_temp: int, day_time: str) -> pd.DataFrame:
    """Filtering by column temperature in degrees Celsius
    Args:
      df: Dataframe with original values
      celsius_temp: temperature in degrees Celsius
    Returns:
      Dataframe with days in which the temperature is not less than the set temperature
    """
    return df[df[f"{day_time} celsius temperature"] >= celsius_temp]


def date_filtration(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """Filtering by date
    Args:
      df: Dataframe with original values
      start_date: date_from
      end_date: End date_to
    Returns:
      Dataframe with days that range [date_from; date_to]
    """
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
    return df[(start_date <= df["Date"]) & (df["Date"] <= end_date)]


# | None:
def group_by_month_with_average_temp(df: pd.DataFrame, parametr: str) -> pd.Series:
    """Grouping by month with calculation of the average temperature value
    Args:
      df: Dataframe with original values
      parametr: A column indicating which temperature is taken
    Returns:
      A series indicating the average value for all months
    """
    if parametr in ["Day celsius temperature", 'Day fahrenheit temperature', 'Night celsius temperature', 'Night fahrenheit temperature']:
        return df.groupby(df.Date.dt.month)[parametr].mean()


def show_temp_graph(df: pd.DataFrame, parametr: str) -> None:
    """Show of the temperature graph for the entire period
    Args:
      df: Dataframe with original values
      parametr: A column indicating which temperature is taken
    """
    if parametr in ["Day celsius temperature", 'Day fahrenheit temperature', 'Night celsius temperature', 'Night fahrenheit temperature']:
        fig = plt.figure(figsize=(19, 5))
        plt.ylabel(parametr)
        plt.xlabel("date")
        plt.title('Изменение температуры')
        plt.plot(df["Date"], df[parametr], color='blue',
                 linestyle='-', linewidth=1)
        plt.show()


def show_temp_graph_median_average(df: pd.DataFrame, param: str, month: int, year: int) -> None:
    """Showing the temperature graph for the specified month in
    the year and displaying the median and average values
    Args:
      df: Dataframe with original values
      month: The month for which the temperature graph is drawn
      year: The year for which the temperature graph is drawn
    """
    month_df = df[(df.Date.dt.month == month) & (df.Date.dt.year == year)]
    fig = plt.figure(figsize=(18, 8))

    fig.add_subplot(1, 3, 1)
    plt.ylabel(f"{param} Celsius temperature")
    plt.xlabel("date")
    plt.plot(month_df.Date.dt.day, month_df[f"{param} celsius temperature"],
             color='blue', linestyle='--', linewidth=2, label='Celsius temperature')
    plt.axhline(y=month_df[f"{param} celsius temperature"].mean(
    ), color='orange', label="Average value")
    plt.axhline(y=month_df[f"{param} celsius temperature"].median(
    ), color='black', label="Median")
    plt.legend(loc=2, prop={'size': 8})

    fig.add_subplot(1, 3, 2)
    plt.ylabel(f"{param} Fahrenheit temperature")
    plt.xlabel("date")
    plt.plot(month_df.Date.dt.day, month_df[f"{param} fahrenheit temperature"],
             color='red', linestyle='--', linewidth=2, label='Fahrenheit temperature')
    plt.axhline(y=month_df[f"{param} fahrenheit temperature"].mean(
    ), color='orange', label="Average value")
    plt.axhline(y=month_df[f"{param} fahrenheit temperature"].median(
    ), color='black', label="Median")
    plt.legend(loc=2, prop={'size': 8})

    plt.show()


df = get_processed_df("dataset.csv")
# print(get_statistical_info(df, "Day celsius temperature"))
# print(celsius_temp_filtration(df, 39, "Day"))
# print(date_filtration(df, "2021-11-11", "2021-11-22"))
# print(group_by_month_with_average_temp(df, "Day celsius temperature"))
# show_temp_graph(df, "Day celsius temperature")
# show_temp_graph_median_average(df, "Day", 11, 2022)
