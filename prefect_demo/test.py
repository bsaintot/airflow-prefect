import pandas as pd
from pandas.util.testing import assert_frame_equal
from prefect import Flow

from prefect.main import concatenate_columns


def test_concatenate_columns_should_create_dataset_with_column_names():
    # Given
    columns_to_concat = [pd.DataFrame([1, 1]), pd.DataFrame([2, 2]), pd.DataFrame([3, 3]),
                         pd.DataFrame([4, 4]), pd.DataFrame([5, 5])]
    expected_dataset = pd.DataFrame({'sepal_length': [1, 1],
                                     'sepal_width': [2, 2],
                                     'petal_length': [3, 3],
                                     'petal_width': [4, 4],
                                     'target': [5, 5]})

    with Flow("An example test flow") as test_flow:
        # When
        actual = concatenate_columns(columns_to_concat)
    state = test_flow.run()
    actual_dataset = state.result[actual].result

    # Then
    assert state.is_successful()
    assert_frame_equal(actual_dataset, expected_dataset)
