import pandas as pd
from google.cloud import bigquery


def prepare_datasets(bq_table_name, gcs_output_path, target_col):
    # Construct a BigQuery client object.
    client = bigquery.Client(project="teak-backup-317206", location="EU")

    # Load data from bigquery
    query = f'SELECT * FROM `{bq_table_name}`'
    dataframe = client.query(query).to_dataframe()

    # Create separate dataset per cover type
    labels = pd.get_dummies(dataframe[target_col], prefix=target_col)
    dataframe = dataframe.drop(target_col, axis=1)

    for column in labels.columns:
        csv_path = f'{gcs_output_path}/{column}/raw_data.csv'
        pd.concat([dataframe, labels[column]], axis=1).to_csv(csv_path, index=False)
