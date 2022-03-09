import xgboost as xgb


def train_model(X_train, y_train,
                n_estimators, learning_rate, scale_pos_weight=1):
    xgb_model = xgb.XGBClassifier(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        scale_pos_weight=scale_pos_weight
    )
    xgb_model.fit(X_train, y_train)

    return xgb_model
