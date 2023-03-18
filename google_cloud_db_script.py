import click
from google.cloud import bigquery


@click.group()
def cli():
    pass


@cli.command()
@click.option("--project-id", prompt=True, help="Google Cloud project ID")
@click.option("--dataset-id", prompt=True, help="BigQuery dataset ID")
def create_tables(project_id, dataset_id):
    """Creates model tables in BigQuery"""
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id)

    # Create tables
    investor_table = bigquery.Table(dataset_ref.table("investors"))
    investor_table.schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("balance", "FLOAT", mode="REQUIRED"),
    ]
    client.create_table(investor_table)

    property_table = bigquery.Table(dataset_ref.table("properties"))
    property_table.schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("description", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("location", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("price", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("active", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("event_id", "STRING", mode="NULLABLE"),
    ]
    client.create_table(property_table)

    event_table = bigquery.Table(dataset_ref.table("events"))
    event_table.schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("description", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("target_amount", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("start_date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("end_date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("amount_raised", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("active", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("locked", "BOOLEAN", mode="REQUIRED"),
        bigquery.SchemaField("bank_account", "STRING", mode="REQUIRED"),
    ]
    client.create_table(event_table)

    investment_table = bigquery.Table(dataset_ref.table("investments"))
    investment_table.schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("investor_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("property_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("amount", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("event_id", "STRING", mode="REQUIRED"),
    ]
    client.create_table(investment_table)

    notification_table = bigquery.Table(dataset_ref.table("notifications"))
    notification_table.schema = [
        bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("event_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("investor_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("message", "STRING", mode="NULLABLE"),
    ]
