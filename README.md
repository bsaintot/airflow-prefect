# Airflow 2.0 vs. Prefect

This R&D / technical watch project was created to compare and benchmark 2 workflow management tools: Airflow 2.0 and Prefect.
Following the [release of Airflow 2.0](https://airflow.apache.org/blog/airflow-two-point-oh-is-here/), this repository
was used as an illustrative / sandbox environment to highlight the main differences that still exist between these solutions
when it comes to the orchestration of machine learning workflows.

You can follow the guidelines below to schedule and orchestrate a dummy data science training workflow based on the 
[iris dataset](https://archive.ics.uci.edu/ml/datasets/iris). This will help you get an idea of the philosophy behind each tool.

## Prefect

Before running the server for the first time, run the following command to configure Prefect for local orchestration:
```bash
prefect backend server
```

Note the server requires Docker and Docker Compose to be running. To start the server, UI, and all required 
infrastructure, run:
````bash
prefect server start
````

Once all components are running, you can view the Prefect UI by visiting http://localhost:8080.

Please note that executing flows from the server requires at least one Prefect Agent to be running:
```bash
prefect agent local start
```

We are now ready to use Prefect Core Server. Let's create a new project for the purpose of this demo:
```bash
prefect create project airflow_prefect_contest
```

Finally, to register any flow with the server, call the register method:
```python
flow.register()
```

## Airflow 2.0

Airflow needs a home, ~/airflow is the default, but you can lay foundation somewhere else if you prefer:
```bash
export AIRFLOW_HOME=~/airflow
```

Initialize the database:
```bash
airflow db init
```

Start the web server. The default port is 8080 but we'll use 8081 to avoid a conflict with Prefect's web server:
```bash
airflow webserver -p 8081
```

You can now view the Airflow UI by visiting http://localhost:8081.

Start the scheduler:
```bash
airflow scheduler
```

Create an admin user account for yourself:
```bash
 airflow users create --username admin
                      --firstname <your-firstname>
                      --lastname <your-lastname>
                      --role Admin
                      --email <your-email>
```
