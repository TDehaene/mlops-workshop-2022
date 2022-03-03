# MLOps Workshop

This repository showcases how to implement reproducible machine learning pipelines with a basic example.

The example is based on the the [Google Notebook](https://github.com/GoogleCloudPlatform/mlops-on-gcp/blob/master/workshops/kfp-caip-sklearn/lab-01-caip-containers/lab-01.ipynb) that is based on the [Covertype dataset](https://archive.ics.uci.edu/ml/datasets/covertype), where the goal is to predict forest cover type (7 categories) from cartographic variables. 

The `setup_bq.sh` and `setup.sh` files are to load the toy dataset in BigQuery and that all necessary services are activated. This is something that only needs to be run once, so you don't need to run it again.

It includes two useful commands:
- `gcloud auth application-default login` - This command will cause a browser window to pop up and ask you to login using you google account. It then sets the necessary variables to make sure all client libraries are able to connect to GCP.
- `gcloud config set project $PROJECT_ID` - This command sets the default project to be used.  


The local folder contains all the code for the first part of the hands-on session. 
It illustrates the starting point of the use case with modularized steps.   

The kfp folder contains all the code for the second part of the hands-on session. 
It illustrates how to take the steps from the previous example and make them into clean reusable components. 
Some changes need to be made to the implementation of the logic of each step, mainly having to do with saving and loading data to and from Cloud Storage at the end and start of each step.   

## Pre-requisites

* [gcloud SDK](https://cloud.google.com/sdk/docs/install)
* [kubectl](https://cloud.google.com/sdk/docs/install)