import pandas as pd
import os

def load_dataset(path=None, time_to_datetime=False):
    '''
    Loads the historical dataset.
    '''
    if not path:
        path = os.path.join('data','train.csv')

    df = pd.read_csv(path)

    if time_to_datetime:
        df['InterventionDateTime'] = pd.to_datetime(df['InterventionDateTime'], infer_datetime_format=True)
    return df

def clean_dataset(df: pd.DataFrame):
    _df = df.copy()

    # select only searched entries
    _df = _df[_df.VehicleSearchedIndicator == True]
    
    # lower location name
    _df.InterventionLocationName = _df.InterventionLocationName.str.lower()
    
    # convert time column to datetime
    _df.InterventionDateTime = pd.to_datetime(_df.InterventionDateTime, infer_datetime_format=True)

    return _df
