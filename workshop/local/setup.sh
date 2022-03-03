# Global variables
export PROJECT_ID="teak-backup-317206"

# Install requirements 
pip install -r requirements.txt

# Create GC bucket
export BUCKET_LOCAL_RUN=${PROJECT_ID}_local-run
gsutil mb -p $PROJECT_ID -l $BUCKET_LOCATION gs://$BUCKET_LOCAL_RUN

