import fire

import config
from helpers.gcloud import gcs_list_dir
from steps.prepare_datasets import prepare_datasets
from train_evaluate import train_evaluate


def run(gcs_bucket, run_name):
    gcs_run_path = f'gs://{gcs_bucket}/{run_name}'
    prepare_datasets(config.DATASET_NAME, gcs_run_path, config.TARGET_COL)

    for cover_type in gcs_list_dir(gcs_bucket, run_name):
        gcs_csv_path = f'{gcs_run_path}/{cover_type}/raw_data.csv'
        gcs_output_path = f'{gcs_run_path}/{cover_type}/output'
        train_evaluate(gcs_csv_path, gcs_output_path)


if __name__ == '__main__':
    fire.Fire(run)
