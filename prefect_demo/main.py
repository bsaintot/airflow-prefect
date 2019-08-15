from prefect import Flow

# from prefect_demo.engine.executors import DaskExecutor
from prefect_demo.tasks import read_column, concatenate_columns, transform, features_extraction, target_extraction, \
    train


with Flow("An example ML flow!") as flow:
    columns = []
    for path in ['col1.csv', 'col2.csv', 'col3.csv', 'col4.csv', 'target.csv']:
        column = read_column('../data/' + path)
        columns.append(column)
    dataset = concatenate_columns(columns)
    transformed_dataset = transform(dataset)
    features = features_extraction(transformed_dataset)
    target = target_extraction(transformed_dataset)
    model = train(features, target)


def main():
    # executor = DaskExecutor(address="tcp://192.168.1.19:8786")
    # state = flow.run(executor=executor)
    state = flow.run()
    flow.visualize(state)
    assert state.is_successful()

    task_result = state.result[model]
    print(task_result.result)


if __name__ == '__main__':
    main()


