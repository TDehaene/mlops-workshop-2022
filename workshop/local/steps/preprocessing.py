from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer


def fit_preprocessor(dataframe,
                     numeric_feature_indexes=slice(0, 10),
                     categorical_feature_indexes=slice(10, 12),
                     ):

    # Set correct dtypes
    num_features_type_map = {
        feature: 'float64' for feature in dataframe.columns[numeric_feature_indexes]
    }
    dataframe = dataframe.astype(num_features_type_map)

    # Preprocess dataframe
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_feature_indexes),
            # Not very many possibilities for categories so sparse is not necessary
            ('cat', OneHotEncoder(sparse=False), categorical_feature_indexes)
        ]
    )
    preprocessor.fit(dataframe)

    return preprocessor
