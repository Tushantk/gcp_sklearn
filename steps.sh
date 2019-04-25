#!/bin/bash
#bashfiledep.sh

echo "Moving Input Data"
gsutil cp gs://modern-heading-234419-modern-heading-234419/train_pickle_deployment.py /home/airflow/gcs/data/
gsutil cp gs://modern-heading-234419-modern-heading-234419/deployment.py /home/airflow/gcs/data/
gsutil cp gs://modern-heading-234419-modern-heading-234419/bashfile.sh /home/airflow/gcs/data/

echo "Download Dependencies"
pip install --upgrade pip --user scikit-learn 
sudo pip install PyMySQL

echo "Building Model"
python /home/airflow/gcs/data/train_pickle_deployment.py

echo "Triggering Bash Script"
bash /home/airflow/gcs/data/bashfile.sh

echo "Deployment Started"
python /home/airflow/gcs/data/deployment.py
