import pandas as pd
import json

import datetime
import holidays

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my_request")
    

def get_cities_latitide(x):
    try:
        return cities_coords[x][0]
    except:
        return 0
    

def get_cities_longitude(x):
    try:
        return cities_coords[x][1]
    except:
        return 0


def get_coordinates_from_city_str(df: pd.DataFrame, city_coords, column: str = 'city') -> pd.DataFrame:
    df['latitude'] = df[column].apply(get_cities_latitide)
    df['longitude'] = df[column].apply(get_cities_longitude)
    return df


def drop_useless_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    try:
        return df.drop(columns, axis=1)
    except:
        pass


def filling_category_data(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for column in columns:
        df = df.fillna({column:df[column].mode()[0]})
    return df


def filling_digital_data(df: pd.DataFrame, column: list) -> pd.DataFrame:
    for column in columns:
        df = df.fillna({column:df[column].mean()[0]})
    return df


def get_spreed_time(df: pd.DataFrame, column: str='created') -> pd.DataFrame:
    df[column] = df[column].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    
    df['year'] = df['created'].apply(lambda x: x.year)
    df['month'] = df['created'].apply(lambda x: x.month)
    df['day'] = df['created'].apply(lambda x: x.day)
    
    df['hour'] = df['created'].apply(lambda x: x.hour)
    df['minute'] = df['created'].apply(lambda x: x.minute)
    df['second'] = df['created'].apply(lambda x: x.second)
    
    df['is_weekend'] = df[column].apply(lambda x: 1 if x.weekday() in (5, 6) else 0)
    
    df['is_holiday'] = df[column].apply(lambda x: 1 if x in holidays.Russia() else 0)
    
    return df


def categorical_data_to_string(df, columns: list) -> pd.DataFrame:
    for column in columns:
        df[column] = df[column].astype('str')
    return df


def preprocess_dataframe(df: pd.DataFrame, cities_coords, test_mode: bool = False) -> pd.DataFrame:
    df = filling_category_data(df, ['gamecategory', 'subgamecategory', 'bundle', 'oblast', 'city'])

    df = get_spreed_time(df)

    df = get_coordinates_from_city_str(df, cities_coords)

    df = drop_useless_columns(df, ['shift', 'created'])

    df = categorical_data_to_string(df, df.columns[1:-2].tolist())

    if test_mode:
        df.drop('Segment', axis=1, inplace=True)

    return df