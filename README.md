# Airflow 2.0 vs. Prefect

## Prefect

Before running the server for the first time, run the following command to configure Prefect for local orchestration. 

Please note the server requires Docker and Docker Compose to be running.

````bash
prefect backend server
````

To start the server, UI, and all required infrastructure, run:

````bash
prefect server start
````

Once all components are running, you can view the UI by visiting http://localhost:8080.

Please note that executing flows from the server requires at least one Prefect Agent to be running:

```bash
prefect agent local start
```

We are now ready to use Prefect Core Server. Let's create a new project for the purpose of this demo:

````bash
prefect create project airflow_prefect_contest
````

Finally, to register any flow with the server, call:

```python
flow.register()
```

## Airflow 2.0

```bash
airflow db init
```

```bash
airflow webserver -p 8081
```

```bash
 airflow users create --username admin
                      --firstname <your-firstname>
                      --lastname <your-lastname>
                      --role Admin
                      --email <your-email>
```

```bash
airflow scheduler
```