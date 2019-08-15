import pandas as pd
from typing import List

from pendulum import pendulum

from airflow_demo.functions import read_column, concatenate_columns, transform, features_extraction, target_extraction, \
    train

COLUMN_PATH = 'column'
DATASET_PATH = 'dataset'
TRANSFORMED_DATASET_PATH = 'transformed_dataset'
FEATURES_PATH = 'features'
TARGET_PATH = 'target'


def read_column_task(file_path: str, column_key: str, **context):
    column = read_column(file_path)

    column_path = _get_unique_temporary_path_from(COLUMN_PATH)
    column.to_parquet(column_path)
    context['task_instance'].xcom_push(key=column_key, value=column_path)


def concatenate_columns_task(columns_to_concat_keys: List[str], dataset_key: str, **context):
    columns = []
    for key in columns_to_concat_keys:
        column_path = context['task_instance'].xcom_pull(key=key)
        column = pd.read_parquet(column_path)
        columns.append(column)

    dataset = concatenate_columns(columns)

    dataset_path = _get_unique_temporary_path_from(DATASET_PATH)
    dataset.to_parquet(dataset_path)
    context['task_instance'].xcom_push(key=dataset_key, value=dataset_path)


def transform_task(dataset_key: str, transformed_dataset_key: str, **context):
    dataset_path = context['task_instance'].xcom_pull(key=dataset_key)
    dataset = pd.read_parquet(dataset_path)

    transformed_dataset = transform(dataset)

    transformed_dataset_path = _get_unique_temporary_path_from(TRANSFORMED_DATASET_PATH)
    transformed_dataset.to_parquet(transformed_dataset_path)
    context['task_instance'].xcom_push(key=transformed_dataset_key, value=transformed_dataset_path)


def features_extraction_task(transformed_dataset_key: str, features_key: str, **context):
    transformed_dataset_path = context['task_instance'].xcom_pull(key=transformed_dataset_key)
    transformed_dataset = pd.read_parquet(transformed_dataset_path)

    features = features_extraction(transformed_dataset)

    features_path = _get_unique_temporary_path_from(FEATURES_PATH)
    features.to_parquet(features_path)
    context['task_instance'].xcom_push(key=features_key, value=features_path)


def target_extraction_task(transformed_dataset_key: str, target_key: str, **context):
    transformed_dataset_path = context['task_instance'].xcom_pull(key=transformed_dataset_key)
    transformed_dataset = pd.read_parquet(transformed_dataset_path)

    target = target_extraction(transformed_dataset)

    target_path = _get_unique_temporary_path_from(TARGET_PATH)
    target.to_parquet(target_path)
    context['task_instance'].xcom_push(key=target_key, value=target_path)


def train_task(features_key: str, target_key: str, **context):
    features_path = context['task_instance'].xcom_pull(key=features_key)
    features = pd.read_parquet(features_path)
    target_path = context['task_instance'].xcom_pull(key=target_key)
    target = pd.read_parquet(target_path)

    model = train(features, target)
    return model


def _get_unique_temporary_path_from(path: str) -> str:
    return path + str(pendulum.utcnow().timestamp())
