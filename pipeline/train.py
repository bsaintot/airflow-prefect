from prefect import Flow, Parameter
from prefect.schedules import Schedule
from prefect.schedules.clocks import CronClock

from iris.tasks import read_column, concatenate_columns, features_extraction, target_extraction, train

sepal_schedule = CronClock('0 * * * *',
                           parameter_defaults=dict(files=['col1.csv', 'col2.csv', 'target.csv']))  # Sepal DAG
petal_schedule = CronClock('0 * * * *',
                           parameter_defaults=dict(files=['col3.csv', 'col4.csv', 'target.csv']))  # Petal DAG
schedule = Schedule(clocks=[sepal_schedule, petal_schedule])

with Flow('Training', schedule=schedule) as flow:
    files = Parameter('files', default=['col1.csv', 'col2.csv', 'target.csv'])

    columns = read_column.map(files)
    dataset = concatenate_columns(columns)
    features = features_extraction(dataset)
    target = target_extraction(dataset)
    train(features, target)

if __name__ == '__main__':
    flow.register(project_name='airflow_prefect_contest')
