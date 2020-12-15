import os
from datetime import timedelta
from typing import List

import pandas as pd
from airflow.decorators import dag
from airflow.operators.python import task
from airflow.utils.dates import days_ago
from sklearn.ensemble import RandomForestClassifier


@task
def read_columns() -> List[pd.DataFrame]:
    columns_to_concat = []
    for file_name in ['col1.csv', 'col2.csv', 'target.csv']:
        absolute_path = os.path.abspath('./data/' + file_name)
        columns_to_concat.append(pd.read_csv(absolute_path, header=None).iloc[:, 0])
    return columns_to_concat


@task
def concatenate_columns(columns_to_concat: List[pd.DataFrame]) -> pd.DataFrame:
    dataset = pd.concat(columns_to_concat, axis=1)
    dataset.columns = ['length', 'width', 'target']
    return dataset


@task
def features_extraction(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset['area'] = dataset['length'] * dataset['width']
    return dataset.drop('target', axis=1)


@task
def target_extraction(dataset: pd.DataFrame) -> pd.Series:
    return dataset['target']


@task
def train(features: pd.DataFrame, target: pd.Series) -> None:
    model = RandomForestClassifier()
    model.fit(features, target)


default_args = {'owner': 'airflow'}


@dag(default_args=default_args, schedule_interval=timedelta(hours=1), start_date=days_ago(2))
def training():
    columns = read_columns()
    dataset = concatenate_columns(columns)
    features = features_extraction(dataset)
    target = target_extraction(dataset)
    train(features, target)


training = training()
