from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from airflow_demo.tasks import read_column_task, concatenate_columns_task, transform_task, features_extraction_task, \
    target_extraction_task, train_task

COL1_KEY = 'col1'
COL2_KEY = 'col2'
COL3_KEY = 'col3'
COL4_KEY = 'col4'
COL5_KEY = 'col5'
DATASET_KEY = 'dataset'
TRANSFORMED_DATASET_KEY = 'transformed_dataset'
FEATURES_KEY = 'features'
TARGET_KEY = 'target'

dag_args = {'dag_id': 'ML-pipeline',
            'description': 'An example ML pipeline',
            'schedule_interval': timedelta(days=1),
            'start_date': datetime(2019, 8, 15),
            'max_active_runs': 1,
            'dagrun_timeout': timedelta(minutes=30),
            'concurrency': 1
            }

dag = DAG(**dag_args)

read_column_1_op = PythonOperator(
    python_callable=read_column_task,
    task_id='read_column_1_task',
    dag=dag,
    provide_context=True,
    op_kwargs={'file_path': 'data/col1.csv', 'column_key': COL1_KEY}
)

read_column_2_op = PythonOperator(
    python_callable=read_column_task,
    task_id='read_column_2_task',
    dag=dag,
    provide_context=True,
    op_kwargs={'file_path': 'data/col2.csv', 'column_key': COL2_KEY}
)

read_column_3_op = PythonOperator(
    python_callable=read_column_task,
    task_id='read_column_3_task',
    dag=dag,
    provide_context=True,
    op_kwargs={'file_path': 'data/col3.csv', 'column_key': COL3_KEY}
)

read_column_4_op = PythonOperator(
    python_callable=read_column_task,
    task_id='read_column_4_task',
    dag=dag,
    provide_context=True,
    op_kwargs={'file_path': 'data/col4.csv', 'column_key': COL4_KEY}
)

read_column_5_op = PythonOperator(
    python_callable=read_column_task,
    task_id='read_column_5_task',
    dag=dag,
    provide_context=True,
    op_kwargs={'file_path': 'data/col5.csv', 'column_key': COL5_KEY}
)

concatenate_columns_op = PythonOperator(
    python_callable=concatenate_columns_task,
    task_id='concatenate_columns_task',
    dag=dag,
    provide_context=True,
    op_kwargs={'columns_to_concat_keys': [COL1_KEY, COL2_KEY, COL3_KEY, COL4_KEY, COL5_KEY], 'dataset_key': DATASET_KEY}
)

transform_op = PythonOperator(
    python_callable=transform_task,
    task_id='transform_task',
    dag=dag,
    provide_context=True,
    op_kwargs={'dataset_key': DATASET_KEY, 'transformed_dataset_key': TRANSFORMED_DATASET_KEY}
)

feature_extraction_op = PythonOperator(
    python_callable=features_extraction_task,
    task_id='feature_extraction_task',
    dag=dag,
    provide_context=True,
    op_kwargs={'transformed_dataset_key': TRANSFORMED_DATASET_KEY}
)

target_extraction_op = PythonOperator(
    python_callable=target_extraction_task,
    task_id='target_extraction_task',
    dag=dag,
    provide_context=True,
    op_kwargs={'transformed_dataset_key': TRANSFORMED_DATASET_KEY}
)

train_op = PythonOperator(
    python_callable=train_task,
    task_id='train_task',
    dag=dag,
    provide_context=True,
    op_kwargs={'features_key': FEATURES_KEY, 'target_key': TARGET_KEY}
)

[read_column_1_op, read_column_2_op, read_column_3_op, read_column_4_op, read_column_5_op] >> concatenate_columns_op
concatenate_columns_op >> transform_op
transform_op >> [feature_extraction_op, target_extraction_op]
[feature_extraction_op, target_extraction_op] >> train_op
