PROJECT_ID=$(gcloud config list project --format "value(core.project)")
BUCKET_NAME=${PROJECT_ID}-modern-heading-234419
echo $BUCKET_NAME
REGION=us-central1



gsutil cp model.joblib  gs://modern-heading-234419-modern-heading-234419/
gsutil cp gs://modern-heading-234419-modern-heading-234419/input.json .
gsutil cp gs://modern-heading-234419-modern-heading-234419/adult.test .



MODEL_DIR="gs://modern-heading-234419-modern-heading-234419/"
INPUT_FILE="input.json"
FRAMEWORK="SCIKIT_LEARN"

echo "Prediction Started"
gcloud ml-engine local predict --model-dir=$MODEL_DIR \
--json-instances $INPUT_FILE \
--framework $FRAMEWORK


echo "Create Model"
###create model name
current_date_time="`date +%Y%m%d%H%M%S`";
MODEL_NAME="version3"

gcloud ml-engine models create $MODEL_NAME


### model version

MODEL_DIR="gs://modern-heading-234419-modern-heading-234419/"
VERSION_NAME="version_new3"

FRAMEWORK="SCIKIT_LEARN"

echo "Versioning Started: Version Name "$VERSION_NAME
gcloud ml-engine versions create $VERSION_NAME \
--model $MODEL_NAME \
--origin $MODEL_DIR \
--runtime-version=1.13 \
--framework $FRAMEWORK \
--python-version=2.7


gcloud ml-engine versions describe $VERSION_NAME \
--model $MODEL_NAME
