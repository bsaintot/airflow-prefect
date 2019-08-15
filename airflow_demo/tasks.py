from typing import List

from airflow_demo.functions import read_column, concatenate_columns, transform, features_extraction, target_extraction, \
    train


def read_column_task(file_path: str, column_key: str, **context):
    column = read_column(file_path)
    context['task_instance'].xcom_push(key=column_key, value=column)


def concatenate_columns_task(columns_to_concat_keys: List[str], dataset_key: str, **context):
    columns = []
    for key in columns_to_concat_keys:
        column = context['task_instance'].xcom_pull(key=key)
        columns.append(column)
    dataset = concatenate_columns(columns)
    context['task_instance'].xcom_push(key=dataset_key, value=dataset)


def transform_task(dataset_key: str, transformed_dataset_key: str, **context):
    dataset = context['task_instance'].xcom_pull(key=dataset_key)
    transformed_dataset = transform(dataset)
    context['task_instance'].xcom_push(key=transformed_dataset_key, value=transformed_dataset)


def features_extraction_task(transformed_dataset_key: str, features_key: str, **context):
    transformed_dataset = context['task_instance'].xcom_pull(key=transformed_dataset_key)
    features = features_extraction(transformed_dataset)
    context['task_instance'].xcom_push(key=features_key, value=features)


def target_extraction_task(transformed_dataset_key: str, target_key: str, **context):
    transformed_dataset = context['task_instance'].xcom_pull(key=transformed_dataset_key)
    target = target_extraction(transformed_dataset)
    context['task_instance'].xcom_push(key=target_key, value=target)


def train_task(features_key: str, target_key: str, **context):
    features = context['task_instance'].xcom_pull(key=features_key)
    target = context['task_instance'].xcom_pull(key=target_key)
    model = train(features, target)
    return model
