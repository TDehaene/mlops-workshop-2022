#!/bin/bash

# Saner programming env: these switches turn some bugs into errors
set -o errexit -o pipefail -o noclobber -o nounset

# Argument parsing
while [[ "$#" -gt 0 ]]; do case $1 in
  -n|--name) name="$2"; shift;;
  -p|--project) project="$2"; shift;;
  *) echo "Unknown parameter passed: $1"; exit 1;;
esac; shift; done

[ -n "${name-}" ] || (echo "Missing required argument '--name'" && exit 1)
[ -n "${project-}" ] || (echo "Missing required argument '--project'" && exit 1)

# Set global variables
REGION="europe-west1"
PROJECT_ID="motorway-ml6"

# Build trainer image
IMAGE_NAME="evaluation"
IMAGE_TAG="latest"
IMAGE_URI="eu.gcr.io/$project/$name/$IMAGE_NAME:$IMAGE_TAG"
gcloud builds submit --tag $IMAGE_URI $IMAGE_NAME
