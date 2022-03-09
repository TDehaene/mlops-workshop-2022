
import numpy as np
import os
import logging

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
    
def preprocess_data():
    
    logging.warning('fetching dataset')

    iris = datasets.load_iris()
    x = iris.data
    y = iris.target
    
    logging.warning('splitting dataset')
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    
    logging.warning('scaling dataset')
    
    std_slc = StandardScaler()
    std_slc.fit(x_train)
    
    x_train_std = std_slc.transform(x_train)
    x_test_std = std_slc.transform(x_test)
    
    logging.warning('saving dataset')
    
    np.save(os.path.join("/opt/ml/processing/train", "x_train.npy"), x_train_std)
    np.save(os.path.join("/opt/ml/processing/train", "y_train.npy"), y_train)
    np.save(os.path.join("/opt/ml/processing/test", "x_test.npy"), x_test_std)
    np.save(os.path.join("/opt/ml/processing/test", "y_test.npy"), y_test)

if __name__ == "__main__":
    preprocess_data()
