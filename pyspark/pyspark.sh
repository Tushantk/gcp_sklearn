
BUCKET_NAME="spark_buck"

PROJECT_ID=$(gcloud config list project --format "value(core.project)")
BUCKET_NAME=${PROJECT_ID}-modern-heading-spark
echo $BUCKET_NAME
REGION=us-central1
gsutil mb -l $REGION gs://$BUCKET_NAME 

gsutil cp model_lg.joblib  gs://modern-heading-234419-modern-heading-spark/

#"testspark.json" example below
#[38, 2, 10, 15, 20, 25]
#[28, 2, 4, 67, 70, 100]

MODEL_DIR="gs://modern-heading-234419-modern-heading-spark/"
INPUT_FILE="testspark.json"
FRAMEWORK="SCIKIT_LEARN"

echo "Prediction Started"
gcloud ml-engine local predict --model-dir=$MODEL_DIR \
--json-instances $INPUT_FILE \
--framework $FRAMEWORK


echo "Create Model"
###create model name
current_date_time="`date +%Y%m%d%H%M%S`";
MODEL_NAME="version9"
gcloud ml-engine models create $MODEL_NAME


### model version

MODEL_DIR="gs://modern-heading-234419-modern-heading-spark/"
VERSION_NAME="version_new9"
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


#test the above model within AI-PLATFORM, model pannel with below data.
# {
  #"instances": [
  #  [38, 2, 10, 15, 20, 25],
  #  [38, 2, 10, 15, 20, 125]
  # ]
#}
