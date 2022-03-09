# Set up and export global variables
export PROJECT_ID="teak-backup-317206"
export USER_NAME="elinaoik"
export REGION="europe-west4"
export BUCKET_LOCATION=EUROPE-WEST4
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# Make sure client libraries can authenticate
gcloud auth application-default login

# Make sure we are working in the correct project
gcloud config set project $PROJECT_ID

# Enable necessary services, this can also be done using Cloud console
gcloud services enable \
aiplatform.googleapis.com \
cloudbuild.googleapis.com \
container.googleapis.com \
cloudresourcemanager.googleapis.com \
iam.googleapis.com \
containerregistry.googleapis.com \
containeranalysis.googleapis.com \
ml.googleapis.com \
dataflow.googleapis.com \
storage.googleapis.com \
bigquery.googleapis.com \
bigquerydatatransfer.googleapis.com \
compute.googleapis.com \

# Update and install gcloud components
gcloud components update &&
gcloud components install beta

#The Cloud Build service account needs the Editor permissions in your GCP project
#to upload the pipeline package to an AI Platform Pipelines instance.
export CLOUD_BUILD_SERVICE_ACCOUNT="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:$CLOUD_BUILD_SERVICE_ACCOUNT \
  --role roles/editor

# The default Compute Engine service account needs editor role
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com \
  --role roles/editor

# Create and connect to a virtual environment
#python3.7 -m venv venv
#source venv/bin/activate

