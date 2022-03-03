#!/bin/bash

# Project Variables
export PROJECT_ID="motorway-ml6"
export USER_NAME="elinaoik"
export BUCKET_LOCATION=EUROPE-WEST4
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# Grand the Compute Engine service account access to Vertex AI
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Configure a Cloud Storage bucket for pipeline artifacts
gsutil mb -p $PROJECT_ID -l $BUCKET_LOCATION gs://${PROJECT_ID}_pipeline-artifacts

# Run the following commands to to grant your service account access to read and write pipeline artifacts
gsutil iam ch \
serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com:roles/storage.objectCreator \
gs://${PROJECT_ID}_pipeline-artifacts

gsutil iam ch \
serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com:roles/storage.objectViewer \
gs://${PROJECT_ID}_pipeline-artifacts

# Install Requirements
pip install -r requirements.txt




  