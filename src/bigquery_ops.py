from config.settings import get_bq_client, PROJECT_ID


def run_query(sql: str):
    client = get_bq_client()
    query_job = client.query(sql)
    return query_job.result()


def create_external_table(
    dataset: str,
    table_name: str,
    source_uri: str,
    source_format: str = "CSV",
):
    client = get_bq_client()
    table_ref = f"{PROJECT_ID}.{dataset}.{table_name}"

    external_config = bigquery.ExternalConfig(source_format)
    external_config.source_uris = [source_uri]

    table = bigquery.Table(table_ref)
    table.external_data_configuration = external_config

    return client.create_table(table, exists_ok=True)


def create_iceberg_table(
    dataset: str,
    table_name: str,
    schema: list,
    storage_uri: str,
    connection_id: str,
):
    client = get_bq_client()
    table_ref = f"{PROJECT_ID}.{dataset}.{table_name}"

    schema_clause = ", ".join(
        f"{col['name']} {col['type']}" for col in schema
    )

    sql = f"""
    CREATE TABLE `{table_ref}`
    ({schema_clause})
    WITH CONNECTION `{connection_id}`
    OPTIONS (
        file_format = "PARQUET",
        table_format = "ICEBERG",
        storage_uri = "{storage_uri}"
    )
    """

    return client.query(sql).result()


def load_data_from_gcs(
    dataset: str,
    table_name: str,
    source_uri: str,
    write_disposition: str = "WRITE_TRUNCATE",
):
    client = get_bq_client()
    table_ref = f"{PROJECT_ID}.{dataset}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=write_disposition,
    )

    load_job = client.load_table_from_uri(
        source_uri, table_ref, job_config=job_config
    )
    return load_job.result()
