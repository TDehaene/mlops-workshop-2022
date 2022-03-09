# MLOps workshop hands-on session 1: AI Platform training

The goal of this first hands-on session is to an example that showcases how to modularize your code. 

A number of very basic ML pipeline steps have already been implemented and can be found in the `steps` folder. These steps are the following:

1) Prepare the datasets: The purpose of this step is to prepare a number of datasets that can be used in the rest of the pipeline. This preparation step will create 1 dataset for each cover type (so 7 datasets in total), where the goal is binary classification of whether an input sample belongs to this cover type or not. The data is read from BigQuery and the resulting datasets are stored in a Google Cloud Storage (GCS) bucket.

2) Split the data: In this step, the input dataset is split into a training and a test set.

3) Preprocessing: Here a very basic sklearn preprocessor is fit that will be used for preprocessing train and test data.

4) Train: An XGboost model is trained and a small number of hyperparameters can be selected.

5) Evaluate: In this final step, the trained model is evaluated (accuracy and f1-score) on the test set.

These basic steps are brought together in the `python train_evaluate.py` script, which runs all these steps and finally prints the evaluation metrics.  

## Running locally

The `run_local.py` script will prepare the datasets and then run the training and evaluation for each different cover type (without hyperparameter tuning). 
The resulting models (preprocessor and xgboost) are stored in a GCS bucket to allow later reuse.   
The command to use in the workshop is: `python run_local.py [YOUR-GCS-BUCKET] [YOUR-NAME]`

