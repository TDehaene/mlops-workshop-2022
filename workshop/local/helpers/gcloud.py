import os
from google.cloud import storage

GCS_CLIENT = storage.Client()


def gcs_list_dir(bucket_name, prefix):
    if prefix[-1] != '/':
        prefix += '/'
    gcs_bucket = GCS_CLIENT.bucket(bucket_name)
    iterator = gcs_bucket.list_blobs(prefix=prefix, delimiter='/')

    prefixes = set()
    for page in iterator.pages:
        prefixes.update(page.prefixes)
    dirs = [prefix.strip('/').split('/')[-1] for prefix in prefixes]

    return dirs


def parse_gcs_path(gcs_path):
    prefix = 'gs://'
    if gcs_path.startswith(prefix):
        parts = gcs_path[len(prefix):].split('/')
    else:
        print('GCS path should start with', prefix)
        exit(1)

    bucket = parts[0]
    path = '/'.join(parts[1:])

    return bucket, path


def upload_file(src_file, gcs_path):
    bucket_name, path = parse_gcs_path(gcs_path)

    gcs_bucket = GCS_CLIENT.bucket(bucket_name)
    gcs_bucket.blob(path).upload_from_filename(src_file)


def download_file(gcs_path, dest_file):
    bucket_name, path = parse_gcs_path(gcs_path)

    gcs_bucket = GCS_CLIENT.bucket(bucket_name)
    gcs_bucket.blob(path).download_to_filename(dest_file)
