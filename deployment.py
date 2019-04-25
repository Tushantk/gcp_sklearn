# Libraries to be installed


import datetime
import pandas as pd

from google.cloud import storage
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelBinarizer
import googleapiclient.discovery
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials


### Public data to be imported


COLUMNS = (
    'age',
    'workclass',
    'fnlwgt',
    'education',
    'education-num',
    'marital-status',
    'occupation',
    'relationship',
    'race',
    'sex',
    'capital-gain',
    'capital-loss',
    'hours-per-week',
    'native-country',
    'income-level'
)

# Categorical columns are columns that need to be turned into a numerical value to be used by scikit-learn
CATEGORICAL_COLUMNS = (
    'workclass',
    'education',
    'marital-status',
    'occupation',
    'relationship',
    'race',
    'sex',
    'native-country'
)

with open('adult.test', 'r') as test_data:
    raw_testing_data = pd.read_csv(test_data, names=COLUMNS, skiprows=1)

test_features = raw_testing_data.drop('income-level', axis=1).as_matrix().tolist()
test_labels = (raw_testing_data['income-level'] == ' >50K.').as_matrix().tolist()


## Update the Project id,model name and version and rfeert to the ML model version

PROJECT_ID = 'modern-heading-234419'
VERSION_NAME = 'version_new3'
MODEL_NAME = 'version3'

service = googleapiclient.discovery.build('ml', 'v1')
name = 'projects/{}/models/{}'.format(PROJECT_ID, MODEL_NAME)
name += '/versions/{}'.format(VERSION_NAME)


## Split the dataset



first_half = test_features[:int(len(test_features)/2)]
second_half = test_features[int(len(test_features)/2):]

complete_results = []
for data in [first_half, second_half]:
    responses = service.projects().predict(
        name=name,
        body={'instances': data}
    ).execute()

    if 'error' in responses:
        print(responses['error'])
    else:
        complete_results.extend(responses['predictions'])

# Print the first 10 responses
for i, responses in enumerate(complete_results[:4]):
    print('Prediction: {}\tLabel: {}'.format(responses, test_labels[i]))
