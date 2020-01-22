import pandas as pd
import numpy as np

from aequitas.group import Group
from aequitas.bias import Bias
from aequitas.fairness import Fairness

def aequitas_preprocessing(df: pd.DataFrame):
    """
    Creates a new dataframe with necessary transformations
    before analyzing with aequitas.
    """


    _df = df.copy()

    # age to bin
    def age_to_bin(age: int) -> str:
        bin_name = ['<21','21-45','>45']
        bins = [0,21,36]

        age_bin = 0 if age < 21 else 1 if age <=45 else 2

        return bin_name[age_bin]

    # Columns and value names to friendly names
    def process_field_names(df):
        """
        Changes field names to friendly names.
        """

        booleanDictionary = {True: 'TRUE', False: 'FALSE'}

        _df = df.copy()
        new_column_names = {'ResidentIndicator':'Is State Resident?', 'TownResidentIndicator':'Is Town Resident?'}
        state_resident_dictionary = {True:'Yes', False:'No'}
        town_resident_dictionary = {True:'Yes', False:'No'}


        sex_dictionary = {'M':'Male', 'F':'Female'}
        race_dictionary = {'W':'White', 'I':'Native', 'B':'Black', 'A':'Asian','U':'Unkown'}

        _df['ResidentIndicator'] = _df['ResidentIndicator'].map(state_resident_dictionary)
        _df['TownResidentIndicator'] = _df['TownResidentIndicator'].map(town_resident_dictionary)
        _df['SubjectSexCode'] = _df['SubjectSexCode'].map(sex_dictionary)
        _df['SubjectRaceCode'] = _df['SubjectRaceCode'].map(race_dictionary)

        _df = _df.rename(columns = new_column_names)

        return _df

    _df = process_field_names(_df)
    _df.SubjectAge = _df.SubjectAge.apply(age_to_bin)

    return _df

def df_to_aequitas(df: pd.DataFrame, model_prediction: str, protected_classes: list =[]):
    '''
    Transforms the dataset into the aequitas format, by:
    1- Creating the 'score' column which represents a binary decision;
    2- Creating the 'label_value' column which is the ground truth of the binary decision;
    3- Selecting categorical columns to be analyzed by aequitas.


    Parameters
    -----------
    model_prediction - column that contains the model prediction
    '''
    aequitas_score_column = 'score'
    aequitas_label_column = 'label_value'

    assert type(protected_classes) == list, 'include_columns must be a list type'
    assert len(protected_classes) > 0, 'You forgot to include categorical columns'
    assert model_prediction in df.columns, 'model_prediction must be included in df columns.'

    _df = df.copy()
    protected_classes_copy = protected_classes[:]
    protected_classes_copy.extend(["ContrabandIndicator", model_prediction])
    _df = _df.filter(protected_classes_copy)
    _df = _df.rename(columns={'ContrabandIndicator': aequitas_label_column,\
                             model_prediction: aequitas_score_column})

    # from False/True to 0/1
    _df[aequitas_score_column] = _df[aequitas_score_column].astype(int)
    _df[aequitas_label_column] = _df[aequitas_label_column].astype(int)

    return _df

def fairness_report(aequitas_df: pd.DataFrame, group_size_threshold : int,fairness_threshold: float, text_report=False):
    """
    Use aequitas to receive a dataframe (in aequitas format) and return
    the subgroups which contain bias results based
    on the false discorery rate.
    """

    # Group scores
    g = Group();
    xtab, _ = g.get_crosstabs(result);

    filtered_xtab = xtab[xtab.group_size > group_size_threshold]

    # Bias through disparity scores
    b = Bias();

    bdf = b.get_disparity_major_group(filtered_xtab,
                                    original_df = result,
                                    label_score_ref='fdr')

    # Fairness through 0.8 threshold on disparity
    f = Fairness(tau=fairness_threshold);
    fdf = f.get_group_value_fairness(bdf);

    failed_fairness = fdf[fdf['FDR Parity'] == False]

    important_columns = ['attribute_name', 'attribute_value','fdr_disparity','fdr_ref_group_value','FDR Parity']

    # return text report of failed fairness
    text_report = True
    if text_report:
        report = "\nFairness Report\n----------\n"
        for idx,row in failed_fairness.iterrows():
            text = f'{row.attribute_name} : {row.attribute_value}\n'
            text += f'It is {round(row.fdr_disparity,2)} times more likely to fail in people who are {row.attribute_value} than people who are {row.fdr_ref_group_value}.\n\n'
            report += text
            return failed_fairness[important_columns],report

    return failed_fairness[important_columns]
