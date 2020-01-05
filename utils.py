import pandas as pd
import os

def load_dataset(path=None):
    '''
    Loads the historical dataset.
    '''
    if not path:
        path = os.path.join('data','train.csv')
        
    df = pd.read_csv(path)
    return df

def aequitas_preprocessing(df: pd.DataFrame, include_columns: list =[]):
    '''
    Transforms the dataset into the aequitas format, by:
    1- Creating the 'score' column which represents a binary decision;
    2- Creating the 'label_value' column which is the ground truth of the binary decision;
    3- Selecting categorical columns to be analyzed by aequitas. 
    '''
    aequitas_score_column = 'score'
    aequitas_label_column = 'label_value'
    
    
    assert include_columns, 'You forgot to include categorical columns'
    
    _df = df.copy()
    include_columns.extend(["ContrabandIndicator", "VehicleSearchedIndicator"])
    _df = _df.filter(include_columns)
    _df = _df.rename(columns={'ContrabandIndicator': aequitas_score_column,\
                             'VehicleSearchedIndicator': aequitas_label_column})
    
    # from False/True to 0/1
    _df[aequitas_score_column] = _df[aequitas_score_column].astype(int)
    _df[aequitas_label_column] = _df[aequitas_label_column].astype(int)
    
    return _df