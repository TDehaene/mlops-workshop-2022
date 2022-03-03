#!/bin/bash

# Saner programming env: these switches turn some bugs into errors
set -o errexit -o pipefail -o noclobber -o nounset

# Argument parsing
while [[ "$#" -gt 0 ]]; do case $1 in
  -n|--name) name="$2"; shift;;
  *) echo "Unknown parameter passed: $1"; exit 1;;
esac; shift; done

[ -n "${name-}" ] || (echo "Missing required argument '--name'" && exit 1)

PROJECT_ID=$(gcloud config get-value core/project)

# Allow caching in Cloud Build, which can greatly speed them up
# See: https://cloud.google.com/cloud-build/docs/speeding-up-builds
gcloud config set builds/use_kaniko True

bash prepare_datasets/build_image.sh --name $name --project $PROJECT_ID
bash split_data/build_image.sh --name $name --project $PROJECT_ID
bash preprocessing/build_image.sh --name $name --project $PROJECT_ID
bash training/build_image.sh --name $name --project $PROJECT_ID
bash evaluation/build_image.sh --name $name --project $PROJECT_ID
