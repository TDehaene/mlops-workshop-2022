import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

from helpers import gcs


def preprocess(gcs_input_path,
               gcs_output_path,
               target_col_prefix,
               numeric_feature_indexes=slice(0, 10),
               categorical_feature_indexes=slice(10, 12),
):
    # Load train and test dataframe from GCS
    train_df = pd.read_csv(f'{gcs_input_path}/train_df.csv')
    test_df = pd.read_csv(f'{gcs_input_path}/test_df.csv')
    
    # Identify column to be predicted
    target_col = [col for col in train_df.columns if col.startswith(target_col_prefix)]
    if len(target_col) != 1:
        print('Ambiguous target column')
    else:
        target_col = target_col[0]
    
    # Prepare train and test targets
    y_train = train_df[target_col].values
    train_df = train_df.drop(target_col, axis=1)
    
    y_test = test_df[target_col].values
    test_df = test_df.drop(target_col, axis=1)
    
    # Set correct dtypes
    num_features_type_map = {
        feature: 'float64' for feature in train_df.columns[numeric_feature_indexes]
    }
    train_df = train_df.astype(num_features_type_map)
    test_df = test_df.astype(num_features_type_map)

    # Preprocess dataframes
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_feature_indexes),
            # Not very many possibilities for categories so sparse is not necessary
            ('cat', OneHotEncoder(sparse=False), categorical_feature_indexes)
        ]
    )
    preprocessor.fit(pd.concat([train_df, test_df]))
    X_train = preprocessor.transform(train_df)
    X_test = preprocessor.transform(test_df)
    
    # Save preprocessed data to GCS
    np.save('X_train.npy', X_train)
    gcs.upload_file('X_train.npy', f'{gcs_output_path}/X_train.npy')
    np.save('y_train.npy', y_train)
    gcs.upload_file('y_train.npy', f'{gcs_output_path}/y_train.npy')
    np.save('X_test.npy', X_test)
    gcs.upload_file('X_test.npy', f'{gcs_output_path}/X_test.npy')
    np.save('y_test.npy', y_test)
    gcs.upload_file('y_test.npy', f'{gcs_output_path}/y_test.npy')
    
    # Save preprocesor to GCS
    joblib.dump(preprocessor, 'preprocessor.joblib')
    gcs.upload_file('preprocessor.joblib', f'{gcs_output_path}/preprocessor.joblib')
