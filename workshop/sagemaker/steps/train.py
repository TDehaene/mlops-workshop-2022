
import numpy as np
import os
import logging
import argparse

from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
    
def train_model(processing_estimator_count, processing_max_depth):
    
    
    logging.warning('Fetching data')
    
    x_train = np.load(os.path.join("/opt/ml/processing/train", "x_train.npy"))
    y_train = np.load(os.path.join("/opt/ml/processing/train", "y_train.npy"))
    
    logging.warning('Training model')
    
    clf=RandomForestClassifier(
        n_estimators=processing_estimator_count,
        max_depth=processing_max_depth)

    clf.fit(x_train, y_train)

    dump(clf, '/opt/ml/processing/model/model.joblib') 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--processing_estimator_count",
        type=str,
        required=True)
    parser.add_argument(
        "--processing_max_depth",
        type=str,
        required=True)
    

    args = parser.parse_args()

    train_model(
        processing_estimator_count=int(args.processing_estimator_count),
        processing_max_depth=int(args.processing_max_depth)
    )
