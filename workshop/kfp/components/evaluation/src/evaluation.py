import numpy as np
import json
import xgboost
from sklearn.metrics import accuracy_score, f1_score
from kfp.v2.dsl import (
    Output,
    Metrics,
    HTML,
)

from helpers import gcs


def evaluate_model(
    gcs_input_path: str,
    metric: Output[Metrics] = None,
    html_metadata: Output[HTML] = None
):
    # Get cover type from gcs input path
    cover_type = gcs_input_path.split('_')[-1]

    # Load test data
    gcs.download_file(f'{gcs_input_path}/X_test.npy', 'X_test.npy')
    X_test = np.load('X_test.npy', allow_pickle=True)
    gcs.download_file(f'{gcs_input_path}/y_test.npy', 'y_test.npy')
    y_test = np.load('y_test.npy', allow_pickle=True)

    # Load model
    gcs.download_file(f'{gcs_input_path}/xgb_model.bin', 'xgb_model.bin')
    xgb_model = xgboost.XGBClassifier()
    xgb_model.load_model('xgb_model.bin')

    # Evaluate the model
    y_pred = xgb_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Dump metrics to file that KFP can pick up to visualise in UI
    # See: https://www.kubeflow.org/docs/pipelines/sdk/pipelines-metrics/
    metrics = {
        'metrics': [
            {
                'name': f'accuracy-{cover_type}',
                'numberValue': acc,
                'format': 'RAW',
            },
            {
                'name': f'f1-score-{cover_type}',
                'numberValue': f1,
                'format': 'RAW',
            }
        ]
    }

    for metric_value in metrics["metrics"]:
        metric.log_metric(
            metric_value['name'], metric_value['numberValue']
        )

    with open('metrics.json', 'w') as f:
        json.dump(metrics, f)

    gcs_metrics_location = f'{gcs_input_path}/metrics.json'
    gcs.upload_file('metrics.json', gcs_metrics_location)

    # Example to show how you can view output in KFP UI
    # See: https://www.kubeflow.org/docs/pipelines/sdk/output-viewer/#introduction
    # In reality, the notebook will be created using the model evaluation output,
    # but here we simply use a readily available notebook in html format
    gcs_notebook_location = f'{gcs_input_path}/notebook.html'
    gcs.upload_file('example_notebook.html', gcs_notebook_location)

    html_metadata._set_path(gcs_notebook_location)
