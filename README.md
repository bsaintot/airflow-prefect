# Airflow 2.0 vs. Prefect

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
