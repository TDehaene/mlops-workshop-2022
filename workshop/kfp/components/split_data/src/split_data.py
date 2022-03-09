import pandas as pd
from sklearn.model_selection import train_test_split as tts


def train_test_split(gcs_input_path, gcs_output_path, test_size=0.2):
    cover_df = pd.read_csv(f'{gcs_input_path}/raw_data.csv')
    
    train_df, test_df = tts(cover_df, test_size=test_size)
    
    train_df.to_csv(f'{gcs_output_path}/train_df.csv', index=False)
    test_df.to_csv(f'{gcs_output_path}/test_df.csv', index=False)
    