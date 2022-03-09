
import numpy as np
import os
import logging
import json
import pathlib

from joblib import dump, load
from sklearn import metrics
    
def eval_model():
    
    logging.warning('Fetching data')
    
    x_test = np.load(os.path.join("/opt/ml/processing/test", "x_test.npy"))
    y_test = np.load(os.path.join("/opt/ml/processing/test", "y_test.npy"))
    
    logging.warning('Fetching model')
    
    clf = load('/opt/ml/processing/model/model.joblib') 
    
    logging.warning('Evaluating model')
    
    y_pred=clf.predict(x_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    
    logging.warning(f"Attained accuracy: {accuracy}")
    
    report_dict = {
        "metrics": {
            "accuracy": {
                "value": accuracy,
            },
        },
    }
    
    output_dir = "/opt/ml/processing/evaluation"
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    evaluation_path = f"{output_dir}/evaluation.json"
    with open(evaluation_path, "w") as f:
        f.write(json.dumps(report_dict))

if __name__ == "__main__":
    eval_model()
