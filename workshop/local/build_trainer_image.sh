# Set global variables
REGION="europe-west1"
PROJECT_ID="smart-amplifier-343007"

# Build trainer image
IMAGE_NAME="trainer_image"
IMAGE_TAG="latest"
IMAGE_URI="eu.gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG"

# Use cloud build to build the image
# This command will take all the files in the current directory (and subdirectories) and send them over to GCP
# It is therefore recommended to make sure there are no unneccesary files in the current directory (or subdirectories),
# since they also get uploaded to GCP. 
# You can also use a .gcloudignore file (like a .gitignore file) to prevent file from being uploaded.
# See: https://cloud.google.com/cloud-build/docs/speeding-up-builds
# Note that because we are using a GCR address as tag, the container image will automatically be available
# in GCR and can be readily used by e.g. AI Platform Training or KFP
gcloud builds submit --tag $IMAGE_URI
