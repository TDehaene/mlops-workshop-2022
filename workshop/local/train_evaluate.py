import os
import tempfile

import fire
import hypertune
import joblib
import numpy as np
import pandas as pd

from helpers.gcloud import gcs_list_dir, upload_file
from steps.preprocessing import fit_preprocessor
from steps.split_data import train_test_split
from steps.train import train_model
from steps.evaluate import evaluate_model


def train_evaluate(gcs_csv_path, gcs_output_path, hptune=False,
                   n_estimators=300, learning_rate=0.1, scale_pos_weight='TRUE'):
    # Load dataframe from GCS
    cover_df = pd.read_csv(gcs_csv_path)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(cover_df)
    n_pos = y_train.sum()
    n_neg = y_train.shape[0] - n_pos

    # Preprocess data
    preprocessor = fit_preprocessor(pd.concat([X_train, X_test]))
    X_train = preprocessor.transform(X_train)

    # Prepare hyperparams and train model
    hparams = {
        'n_estimators': n_estimators,
        'learning_rate': learning_rate
    }
    if scale_pos_weight in ('TRUE', 'True', 'true'):
        hparams['scale_pos_weight'] = n_neg / n_pos
    clf = train_model(X_train, y_train, **hparams)

    # Evaluate model on test set
    X_test = preprocessor.transform(X_test)
    acc, f1 = evaluate_model(clf, X_test, y_test)
    print(
        f'n_pos: {n_pos} - n_neg {n_neg}'
        f'\tAccuracy: {acc} \t F1-score: {f1}'
    )

    # Report metric to cloud hypertune
    if hptune:
        hpt = hypertune.HyperTune()
        hpt.report_hyperparameter_tuning_metric(
            hyperparameter_metric_tag='f1-score',
            metric_value=f1
        )
    # Train model on all data and save to GCS
    else:
        clf = train_model(np.append(X_train, X_test, axis=0),
                          np.append(y_train, y_test),
                          **hparams)

        # Save clf and preprocessor
        with tempfile.TemporaryDirectory() as tmpdir:
            clf.save_model(f'{tmpdir}/xgboost.bin')
            joblib.dump(preprocessor, f'{tmpdir}/preprocessor.joblib')

            upload_file(f'{tmpdir}/xgboost.bin', f'{gcs_output_path}/xgboost.bin')
            upload_file(f'{tmpdir}/preprocessor.joblib', f'{gcs_output_path}/preprocessor.joblib')


if __name__ == '__main__':
    fire.Fire(train_evaluate)
