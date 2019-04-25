# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example DAG demonstrating simple Apache Airflow operators."""

# [START composer_simple]
from __future__ import print_function

# [START composer_simple_define_dag]
import datetime

from airflow import models
# [END composer_simple_define_dag]
# [START composer_simple_operators]
from airflow.operators import bash_operator
from airflow.operators import python_operator
# [END composer_simple_operators]


yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    'start_date': yesterday,
    # To email on failure or retry set 'email' arg to your email and enable
    # emailing here.
    'email_on_failure': False,
    'email_on_retry': False,
    # If a task fails, retry it once after waiting at least 5 minutes
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'project_id': models.Variable.get('gcp_project')
}

dep_command = "/home/airflow/gcs/data/steps.sh "

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.
with models.DAG(
        'gcp_sklearn',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:
    # [END composer_simple_define_dag]
    # [START composer_simple_operators]
    def greeting():
        import logging
        logging.info('Logger || GCP sklearn Implementation')

    # An instance of an operator is called a task. In this case, the
    # hello_python task calls the "greeting" Python function.
    log_python = python_operator.PythonOperator(
        task_id='start',
        python_callable=greeting)
	# Likewise, the goodbye_bash task calls a Bash script.
    copy_steps = bash_operator.BashOperator(
        task_id='copy_steps',
        bash_command='gsutil cp gs://modern-heading-234419-modern-heading-234419/steps.sh /home/airflow/gcs/data/')
    # [END composer_simple_operators]
    # Likewise, the goodbye_bash task calls a Bash script.
    deployment_bash = bash_operator.BashOperator(
        task_id='build_model',
        bash_command=dep_command)
    # [END composer_simple_operators]

    # [START composer_simple_relationships]
    # Define the order in which the tasks complete by using the >> and <<
    # operators. In this example, hello_python executes before goodbye_bash.
    log_python >> copy_steps >> deployment_bash
    # [END composer_simple_relationships]
# [END composer_simple]