import os
import sys
import itertools
from operator import add
from pyspark.ml import Pipeline
from os.path import join, isfile, dirname
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.ml import Pipeline, PipelineModel
#from sparknlp.annotator import *
#from sparknlp.base import DocumentAssembler, Finisher
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import UserDefinedFunction
from pyspark.mllib.regression import LabeledPoint
from pyspark.ml.classification import LogisticRegression
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import OneHotEncoderEstimator, StringIndexer, VectorAssembler
from pyspark.sql.types import IntegerType
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler

CLOUDSQL_INSTANCE_IP = '35.184.7.191'   # CHANGE (database server IP)
CLOUDSQL_DB_NAME = 'sklearn_data'
CLOUDSQL_USER = 'root'
CLOUDSQL_PWD  = 'root'  # CHANGE

conf = SparkConf().setAppName("spark_model")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

jdbcDriver = 'com.mysql.jdbc.Driver'
jdbcUrl    = 'jdbc:mysql://%s:3306/%s?user=%s&password=%s' % (CLOUDSQL_INSTANCE_IP, CLOUDSQL_DB_NAME, CLOUDSQL_USER, CLOUDSQL_PWD)

# checkpointing helps prevent stack overflow errors
sc.setCheckpointDir('checkpoint/')

# Read the ratings and accommodations data from Cloud SQL
df = sqlContext.read.format('jdbc').options(driver=jdbcDriver, url=jdbcUrl, dbtable='spark_data', useSSL='false').load()
#print('read...')
#df.show(2)
#numeric_features = [t[0] for t in df.dtypes if t[1] == 'int']
#df.select(numeric_features).describe().toPandas().transpose()
df = df.select('age','job','marital','education','defaulters','balance','housing','loan','contact','day','month','duration','campaign','pdays','previous','poutcome','deposit')

df1 = df.na.drop()

categorical_columns= ['job','marital','education','housing','loan','contact','day','month','poutcome','deposit']

# The index of string vlaues multiple columns
indexers = [
    StringIndexer(inputCol=c, outputCol="{0}_indexed".format(c))
    for c in categorical_columns
]

# The encode of indexed vlaues multiple columns
encoders = [OneHotEncoder(dropLast=False,inputCol=indexer.getOutputCol(),
            outputCol="{0}_encoded".format(indexer.getOutputCol())) 
    for indexer in indexers
]

# Vectorizing encoded values
assembler = VectorAssembler(inputCols=[encoder.getOutputCol() for encoder in encoders],outputCol="features")

pipeline = Pipeline(stages=indexers + encoders+[assembler])
model=pipeline.fit(df1)
transformed = model.transform(df1)


# write them
schema = StructType([StructField("age", IntegerType(), True), StructField("job", StringType(), True), StructField("marital", StringType(), True),
StructField("education", StringType(), True),StructField("defaulters", StringType(), True),StructField("balance", IntegerType(), True),StructField("housing", StringType(), True),
StructField("loan", StringType(), True),StructField("contact", StringType(), True),StructField("duration", IntegerType(), True),
StructField("campaign", IntegerType(), True),StructField("pdays", IntegerType(), True),StructField("previous", IntegerType(), True),StructField("poutcome", StringType(), True),
StructField("deposit", StringType(), True),StructField("job_indexed", IntegerType(), True),StructField("marital_indexed", IntegerType(), True),StructField("education_indexed", IntegerType(), True)])


#dfToSave = sqlContext.createDataFrame(allPredictions, schema)
dfToSave = sqlContext.createDataFrame(transformed.rdd.map(lambda x: (x.age,x.job,x.marital,x.education,x.defaulters,x.balance,x.housing,x.loan,x.contact,x.duration,x.campaign,x.pdays,x.previous,x.poutcome,x.deposit,x.job_indexed,x.marital_indexed,x.education_indexed),schema))
dfToSave.write.jdbc(url=jdbcUrl, table='Rec', mode='overwrite')

