from typing import List
import pandas as pd
from prefect import task
from sklearn.ensemble import RandomForestClassifier


@task
def read_column(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path, header=None).iloc[:, 0]


@task
def concatenate_columns(columns_to_concat: List[pd.DataFrame]) -> pd.DataFrame:
    dataset = pd.concat(columns_to_concat, axis=1)
    dataset.columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "target"]
    return dataset


@task
def transform(dataset: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([dataset, dataset, dataset], axis=0)


@task
def features_extraction(transformed_dataset: pd.DataFrame) -> pd.DataFrame:
    transformed_dataset["sepal_area"] = transformed_dataset["sepal_length"] * transformed_dataset["sepal_width"]
    transformed_dataset["petal_area"] = transformed_dataset["petal_length"] * transformed_dataset["petal_width"]
    return transformed_dataset.drop("target", axis=1)


@task
def target_extraction(transformed_dataset: pd.DataFrame) -> pd.Series:
    return transformed_dataset["target"]


@task
def train(features: pd.DataFrame, target: pd.Series) -> RandomForestClassifier:
    rf = RandomForestClassifier()
    rf.fit(features, target)
    return rf
