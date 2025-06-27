import requests
from datetime import datetime
from airflow import DAG
from airflow.decorators import task


with DAG(
        schedule="0 9 * * *",  # Daily at 9 AM
        start_date=datetime(2025, 1, 1),
        dag_id="regularly_scrape_deck") as dag:

    @task()
    def scrape_deck():
        requests.get("http://host.docker.internal:8000/decks")

    scrape_deck()

