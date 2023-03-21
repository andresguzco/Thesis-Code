import pandas as pd


def get_clean_data(path: str) -> pd.DataFrame:
    """
    :param path: filepath to the raw data
    :return: Pandas DataFrame with the raw data
    """
    return pd.read_csv(path, index_col=0)


def matrix_creator(input_df: pd.DataFrame, geo_level: str) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    :param input_df: dataset with the raw data
    :param geo_level: granularity for the geographical division
    :return: three dataframes, each containing one the individual data for a variable
    """

    if geo_level == "street":
        geo_att = "name"
    else:
        geo_att = "tag"

    df = input_df.drop(columns=["latitude", "longitude"]).copy(deep=True)
    unique_names = df[geo_att].unique()

    df_pol = pd.DataFrame(df.loc[df[geo_att] == unique_names[0], "pm25"])
    df_pol.rename(columns={"pm25": unique_names[0]}, inplace=True)
    df_wind = pd.DataFrame(df.loc[df[geo_att] == unique_names[0], "Wind Speed"])
    df_wind.rename(columns={"Wind Speed": unique_names[0]}, inplace=True)
    df_angle = pd.DataFrame(df.loc[df[geo_att] == unique_names[0], "Wind Angle"])
    df_angle.rename(columns={"Wind Angle": unique_names[0]}, inplace=True)

    for i in range(1, len(unique_names)):
        df_pol = df_pol.combine_first(pd.DataFrame(df.loc[df[geo_att] == unique_names[i], "pm25"]))
        df_pol.rename(columns={"pm25": unique_names[i]}, inplace=True)

        df_wind = df_wind.combine_first(pd.DataFrame(df.loc[df[geo_att] == unique_names[i], "Wind Speed"]))
        df_wind.rename(columns={"Wind Speed": unique_names[i]}, inplace=True)

        df_angle = df_angle.combine_first(pd.DataFrame(df.loc[df[geo_att] == unique_names[i], "Wind Angle"]))
        df_angle.rename(columns={"Wind Angle": unique_names[i]}, inplace=True)

    for column in df_pol:
        median_values = (df_pol[column].median(), df_angle[column].median(), df_wind[column].median())
        df_pol[column].fillna(value=median_values[0], inplace=True)
        df_angle[column].fillna(value=median_values[1], inplace=True)
        df_wind[column].fillna(value=median_values[2], inplace=True)

    return df_pol, df_wind, df_angle

