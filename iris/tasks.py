import os
from datetime import timedelta
from typing import List

import pandas as pd
from prefect import task
from sklearn.ensemble import RandomForestClassifier


@task(max_retries=3, retry_delay=timedelta(seconds=10))
def read_column(file_name: str) -> pd.DataFrame:
    absolute_path = os.path.abspath('./data/' + file_name)
    return pd.read_csv(absolute_path, header=None).iloc[:, 0]


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
