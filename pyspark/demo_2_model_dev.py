import datetime
import pandas as pd
import pymysql
import pymysql.cursors
from os import getenv
import sqlalchemy
from google.cloud import storage
from sklearn.externals import joblib
from google.cloud import storage
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelBinarizer
import googleapiclient.discovery
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

BUCKET_NAME = 'heading-234419-sklearn_poc'

# TODO(developer): specify SQL connection details

CONNECTION_NAME = getenv(
  'INSTANCE_CONNECTION_NAME',
  'modern-heading-234419:us-central1:sklearndata-1')
DB_USER = getenv('MYSQL_USER', 'root')
DB_PASSWORD = getenv('MYSQL_PASSWORD', 'root')
DB_NAME = getenv('MYSQL_DATABASE', 'sklearn_data')

mysql_config = {
  'host': '35.184.7.191',
  'user': DB_USER,
  'password': DB_PASSWORD,
  'db': DB_NAME,
  'charset': 'utf8mb4',
  'cursorclass': pymysql.cursors.DictCursor,
  'autocommit': True
}

database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(DB_USER, DB_PASSWORD,
                                                      '35.184.7.191', DB_NAME))


connection = pymysql.connect(**mysql_config)

connection1 = database_connection.connect()

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM Rec limit 10"
        cursor.execute(sql)
        sql_data = pd.DataFrame(cursor.fetchmany(10))

        sql_data = sql_data.rename(columns = {'_15':'deposit'})
        sql_data = sql_data.rename(columns = {'_14':'poutcome'})
        sql_data = sql_data.rename(columns = {'_13':'previous'})
        sql_data = sql_data.rename(columns = {'_12':'pdays'})
        sql_data = sql_data.rename(columns = {'_11':'campaign'})
        sql_data = sql_data.rename(columns = {'_10':'duration'})
        sql_data = sql_data.rename(columns = {'_9':'contact'})
        sql_data = sql_data.rename(columns = {'_8':'loan'})
        sql_data = sql_data.rename(columns = {'_7':'housing'})
        sql_data = sql_data.rename(columns = {'_6':'balance'})
        sql_data = sql_data.rename(columns = {'_5':'defaulters'})
        sql_data = sql_data.rename(columns = {'_4':'education'})
        sql_data = sql_data.rename(columns = {'_3':'marital'})
        sql_data = sql_data.rename(columns = {'_2':'job'})
        sql_data = sql_data.rename(columns = {'_1':'age'})
        sql_data = sql_data.rename(columns = {'_16':'job_indexed'})
        sql_data = sql_data.rename(columns = {'_17':'marital_indexed'})
        sql_data = sql_data.rename(columns = {'_18':'education_indexed'})

        sql_data1 = sql_data[['age','duration','campaign', 'pdays','previous','balance','defaulters']]
        
        from sklearn.preprocessing import LabelEncoder

        lb = LabelEncoder() 
        sql_data1['defaulters'] = lb.fit_transform(sql_data1['defaulters'])


        X_train, X_test, y_train, y_test = train_test_split(sql_data1.loc[:, sql_data1.columns != 'defaulters'], 
                                                    sql_data1.defaulters, test_size=0.2, random_state =1234)


        train_features = X_train.values.tolist()
        test_features = X_test.values.tolist()

        train_labels = y_train.values.tolist()

        test_labels = y_test.values.tolist()

        first_half = train_features[:int(len(train_features))]
        second_half = test_features[:int(len(test_features))]


        model_lg = LogisticRegression()
        model_lg.fit(first_half, train_labels)
        y_pred = model_lg.predict(second_half)

        model_lg = 'model_lg.joblib'
        joblib.dump(model_lg, model_lg)
        #loaded_model = joblib.load(model_lg)

        bucket = storage.Client().bucket(BUCKET_NAME)
        blob = bucket.blob('{}/{}'.format(
             datetime.datetime.now().strftime('pyspark_%Y%m%d_%H%M%S'),
             model_lg))
        blob.upload_from_filename(model_lg)

        print(y_pred)


finally:
    connection.close()