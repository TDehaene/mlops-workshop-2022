# Global variables
export PROJECT_ID="smart-amplifier-343007"

# Install requirements 
pip install -r requirements.txt

# Create GC bucket
export BUCKET_LOCATION=europe-west1-b
export BUCKET_LOCAL_RUN=${PROJECT_ID}-modeltraining
gsutil mb -p $PROJECT_ID -l $BUCKET_LOCATION gs://$BUCKET_LOCAL_RUN
