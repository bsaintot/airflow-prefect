from setuptools import setup, find_packages

setup(
    name='airflow-prefect',
    version='1.0.0',
    url='https://gitlab.com/bsaintot/airlflow-prefect',
    author='BASA',
    author_email='basa@octo.com',
    description='An illustrated comparison of Prefect and Airflow 2.0',
    packages=find_packages(),
    install_requires=['apache-airflow==2.0.0rc3',
                      'pandas>=1.1.3',
                      'prefect==0.13.19',
                      'scikit-learn>=0.23.2',
                      'werkzeug==0.16.1'],
)
