import os
import pandas as pd
import json


def get_project_config(cfg_file: str = 'project.json'):
    "This function get general project config values"
    with open("cfg/" + cfg_file, encoding='utf-8') as json_file:
        pcfg = json.load(json_file)
    return pcfg


def missing_values_(df: pd.DataFrame):
    total = df.isnull().sum().sort_values(ascending=False)
    percent = round((100 * df.isnull().sum()/df.isnull().count()).sort_values(ascending=False),2)
    missing_data = pd.concat([total, percent], axis=1, keys=['Cnt', 'Percent']).sort_values(by='Percent', ascending=False)
    return missing_data[missing_data['Cnt']!=0]


def missing_values(df: pd.DataFrame, threshold=0, asc_sorting=False):
    """
        Calculate the missing (NaN) values and their percentage in the given DataFrame.

        Args:
        - df (pd.DataFrame): The DataFrame to be examined.
        - threshold (float, optional): Threshold percentage for missing values.
            Default is 0.

        Returns:
        - pd.DataFrame: A DataFrame containing the count and percentage of missing values.
            If a threshold is specified, it includes missing values with a percentage below
            the specified threshold.
    """
    total = df.isnull().sum().sort_values(ascending=False)
    percent = round((df.isnull().sum()/df.isnull().count() * 100), 5)
    df_missing_data = pd.concat([total, percent], axis=1, keys=['Count', 'Percent']).sort_values(by='Percent', ascending=asc_sorting)
    df_missing_data.index.name = 'Columns'
    # df_missing_data.reset_index(inplace=True)

    # if threshold == 0:
    #     return df_missing_data
    # else:
    #     # return df_missing_data[df_missing_data['Percent'] <= threshold]
    #     return df_missing_data[df_missing_data['Percent'] >= threshold]
    return df_missing_data[df_missing_data['Percent'] >= threshold]


def detect_cardinality(df: pd.DataFrame):
    """
        Detects the cardinality (number of unique values) for each feature in the given DataFrame.

        Args:
        - df (pd.DataFrame): The DataFrame for which cardinality is to be calculated.

        Returns:
        - pd.DataFrame: A DataFrame containing the cardinality count for each feature.
    """
    feature_cardinality = {}

    for column in df.columns:
        cardinality_value = df[column].nunique()
        feature_cardinality[column] = cardinality_value
    df_card_data = pd.DataFrame.from_dict(data=feature_cardinality, orient='index', columns=['NUniqueCount'])
    # df_card_data['Percent'] = round(((df_card_data.shape[0]/df_card_data['NUniqueCount']) * 100), 5)
    df_card_data['Count'] = df.count()
    df_card_data.index.name = 'Columns'

    return df_card_data


def delete_outlier(df: pd.DataFrame, colname: str, k: int = 1.5):
    q1 = df[colname].quantile(0.25)
    q3 = df[colname].quantile(0.75)
    iqr = q3 - q1

    # print("Q1 Quantile Value:", q1)
    # print("Q3 Quantile Value:", q3)
    # print("IQR Value:", iqr)

    lower_bound = q1 - k * iqr
    upper_bound = q3 + k * iqr
    # print("Lower Bound:", lower_bound)
    # print("Upper Bound:", upper_bound)
    return df[(df[colname] > lower_bound) & (df[colname] < upper_bound)]


def cumulative_percentage(df: pd.DataFrame, col_name: str, thres: int = 90):
    df_data_cum = pd.DataFrame()
    df_data_cum[str(col_name) + str('_Cnt')] = pd.DataFrame(df[col_name].value_counts(normalize=False))
    df_data_cum[str(col_name) + str('_CumSum')] = pd.DataFrame(df[col_name].value_counts(normalize=False)).cumsum()
    df_data_cum[str(col_name) + str('_CumSumPercent')] = round(df[col_name].value_counts(normalize=False).cumsum()/df[col_name].value_counts(normalize=False).sum()*100, 2)
    return df_data_cum[df_data_cum[str(col_name) + str('_CumSumPercent')] <= thres].reset_index().rename(columns={'index': col_name})


def create_date_features(df: pd.DataFrame, columns: list = []):
    for column in columns:
        df[column + '_Yil'] = df[column].dt.year
        df[column + '_Ay'] = df[column].dt.month
        df[column + '_Gun'] = df[column].dt.day
        df[column + '_YilKGun'] = df[column].dt.dayofyear
        # df[column + '_YilKHafta'] = df[column].dt.weekofyear
        df[column + '_YilKHafta'] = df[column].dt.isocalendar().week
        df[column + '_HaftaKGun'] = df[column].dt.dayofweek + 1
        df[column + '_HaftaSonu'] = df[column].dt.weekday // 5
        # df[column + '_HaftaSonuA'] = df[column].dt.weekday >= 5
        df[column + '_AyBasi'] = df[column].dt.is_month_start.astype(int)
        df[column + '_AySonu'] = df[column].dt.is_month_end.astype(int)
    return df


def create_date_base_features(df: pd.DataFrame, columns: list = []):
    for column in columns:
        df[column + '_YEAR'] = df[column].dt.year
        df[column + '_MONTH'] = df[column].dt.month
        df[column + '_DAY'] = df[column].dt.day
        df[column + '_DAYOFYEAR'] = df[column].dt.dayofyear

        # df[column + '_WEEKOFYEAR'] = df[column].dt.weekofyear
        df[column + '__WEEKOFYEAR'] = df[column].dt.isocalendar().week

        df[column + '_DAYOFWEEK'] = df[column].dt.dayofweek + 1
        df[column + '_ISWEEKEND'] = df[column].dt.weekday // 5
        # df[column + '_ISWEEKENDA'] = df[column].dt.weekday >= 5
        df[column + '_ISMONTHSTART'] = df[column].dt.is_month_start.astype(int)
        df[column + '_ISMONTHEND'] = df[column].dt.is_month_end.astype(int)
    return df
