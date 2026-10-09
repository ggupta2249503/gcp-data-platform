from config.settings import get_gcs_client


def upload_file(bucket_name: str, source_file: str, destination_blob: str):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_file)
    return f"gs://{bucket_name}/{destination_blob}"


def download_file(bucket_name: str, source_blob: str, destination_file: str):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob)
    blob.download_to_filename(destination_file)
    return destination_file


def list_files(bucket_name: str, prefix: str = ""):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    return [blob.name for blob in bucket.list_blobs(prefix=prefix)]


def delete_file(bucket_name: str, blob_name: str):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    return f"Deleted gs://{bucket_name}/{blob_name}"
