#!/bin/bash
#bashfiledep.sh

echo "Moving Input Data"
gsutil cp gs://heading-234419-sklearn_poc/pyspark.sh /home/airflow/gcs/data/
gsutil cp gs://heading-234419-sklearn_poc/demo_2_deployment.py /home/airflow/gcs/data/
gsutil cp gs://heading-234419-sklearn_poc/demo_2_model_dev.py /home/airflow/gcs/data/
gsutil cp gs://heading-234419-sklearn_poc/model_deploy.py /home/airflow/gcs/data/



echo "Download Dependencies"
#pip install --upgrade pip --user scikit-learn
pip install -U scikit-learn==0.20.3 --user
pip install --user joblib
pip install --user flask
pip install --user sqlalchemy
pip install --user mysql-connector
sudo pip install PyMySQL
sudo pip install mysql-connector
sudo apt-get install mysql-client
