REGION=eu-central-1
ACCOUNT_ID=057384803197

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

docker build -t $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/mlops-training-image:latest .

docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/mlops-training-image:latest