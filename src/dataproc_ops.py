from google.cloud import dataproc_v1
from config.settings import PROJECT_ID, REGION


def submit_spark_job(
    main_python_file_uri: str,
    args: list = None,
    batch_id: str = None,
):
    client = dataproc_v1.BatchControllerClient(
        client_options={"api_endpoint": f"{REGION}-dataproc.googleapis.com:443"}
    )

    batch = {
        "spark_batch": {
            "python_file_uris": [main_python_file_uri],
            "args": args or [],
        },
        "environment_config": {
            "execution_config": {
                "ttl": {"seconds": 3600},
            },
        },
    }

    if batch_id:
        batch_id = batch_id
    else:
        import time
        batch_id = f"spark-job-{int(time.time())}"

    parent = f"projects/{PROJECT_ID}/locations/{REGION}"

    operation = client.create_batch(
        parent=parent,
        batch=batch,
        batch_id=batch_id,
    )

    return operation
