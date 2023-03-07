import pandas as pd
import numpy as np
import math


def angle_correction(angle) -> int:
    if angle > 360:
        angle -= 360
        angle = angle_correction(angle)
    return angle


def get_data(filepath: str) -> pd.DataFrame:
    """
    This is a temporal function while using a snapshot of the data being gathered by
    Hollandse Luchten. The upcoming update substitutes this functions with a connection
    to the API. This will allow for constant sourcing of data.

    :param filepath: Local filepath to the raw dataset
    :return: Pandas DataFrame with the raw data
    """
    return pd.read_csv(filepath)


def format_data(df_input: pd.DataFrame) -> pd.DataFrame:
    """
    :param df_input: Raw data from Hollandse Luchten formatting
    :return: Source data set with variables of interest
    """
    df = df_input.copy()
    df["FH"] = df["FH"] * 0.36
    df.drop(['id', 'no2', 'pm10', 'pm10_cal', 'pm10_fac', 'pm10_max', 'pm10_min', 'pm25_cal',
            'datum', 'tijd', 'pm25_fac', 'pm25_max', 'pm25_min', 'components', 'sensortype',
            'weekdag', 'uur', '#STN', 'jaar', 'maand', 'weeknummer', 'dag', 'H', 'T', 'U'],
            axis=1, inplace=True)

    for row in df.itertuples():
        index, DD_value = row.Index, row.DD
        df.at[index, 'DD'] = angle_correction(row.DD)

    df.rename(columns={"DD": "Wind Angle", "FH": "Wind Speed"}, inplace=True)

    return df


def group_data(df, geo_level: str, time_interval: str) -> pd.DataFrame:

    """
    :param df:
    :param geo_level:
    :param time_interval:
    :return:
    """

    if geo_level == "street":
        geo_group = "name"
    else:
        geo_group = "tag"

    if time_interval == "days":
        time_group = "YYYYMMDD"
    else:
        time_group = "timestamp"

    grouped_df = df.groupby(by=[geo_group, time_group]).median().copy().reset_index()
    grouped_df["Date"] = pd.to_datetime(grouped_df[time_group].astype(str))
    grouped_df.drop(columns=["YYYYMMDD", "timestamp"], inplace=True)
    grouped_df.set_index("Date", inplace=True)

    return grouped_df