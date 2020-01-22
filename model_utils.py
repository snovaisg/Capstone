import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin

class Selector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a column from the dataframe to perform additional transformations on
    """
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self


class CategorySelector(Selector):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on category columns in the data
    """
    def transform(self, X):
        return X[self.key]

class TimeSelector(Selector):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    a datetime column
    """
    def transform(self, X):
        return X[self.key]

class ExtractTimeFeatures(TransformerMixin):
    """
    Transformer to process datetime column.
    """
    def transform(self, X, *_):
        _X = pd.DataFrame(data=X.values,index=X.index,columns=['time'])
        _X['hour'] = _X.time.dt.hour
        return _X[['hour']]

    def fit(self, *_):
        return self

def create_predictions_dataframe(df: pd.DataFrame, preds: np.array)->pd.DataFrame:
    """
    Creates predictions dataframe with original features and a new column "Predictions"
    that replaces the "VehicleSearchedIndicator" column with the model predictions.
    """
    _df = df.copy()
    predictions_df = _df.copy()
    predictions_df = predictions_df.drop(columns=['VehicleSearchedIndicator'])
    columns = list(predictions_df.columns)
    predictions_df = predictions_df.assign(Prediction=preds)
    predictions_df = predictions_df[['Prediction']+columns]
    return predictions_df