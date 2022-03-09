from sklearn.model_selection import train_test_split as tts


def train_test_split(dataframe, target_col_prefix='Cover_Type', test_size=0.2):
    target_col = [col for col in dataframe.columns if col.startswith(target_col_prefix)]
    if len(target_col) != 1:
        print('Ambiguous target column')
    else:
        target_col = target_col[0]

    labels = dataframe[target_col]
    dataframe = dataframe.drop(target_col, axis=1)

    return tts(dataframe, labels, test_size=test_size)
