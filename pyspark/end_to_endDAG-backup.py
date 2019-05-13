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
from airflow.contrib.operators import dataproc_operator
from airflow.operators import python_operator
from airflow.utils import trigger_rule
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
pysparkFile = (
    'gs://heading-234419-sklearn_poc/spark_latest.py'
)
dep_command = "/home/airflow/gcs/data/steps-end-to-end.sh "
dep_command_1 = "/home/airflow/gcs/data/pyspark.sh "

# Define a DAG (directed acyclic graph) of tasks.
# Any task you create within the context manager is automatically added to the
# DAG object.
with models.DAG(
        'gcp_sklearn_end_to_end_flow-test',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:
    # [END composer_simple_define_dag]

    # An instance of an operator is called a task. In this case, the

	# Likewise, the goodbye_bash task calls a Bash script.
    create_dataproc_cluster = dataproc_operator.DataprocClusterCreateOperator(
        task_id='create_dataproc_cluster',
        # Give the cluster a unique name by appending the date scheduled.
        # See https://airflow.apache.org/code.html#default-variables
        cluster_name='spark-data-cluster-{{ ds_nodash }}',
        num_workers=2,
        image_version='1.4',
        init_actions_uris=['gs://heading-234419-sklearn_poc/startup-with-numpy-1-4-image.sh'],
        service_account_scopes=['https://www.googleapis.com/auth/cloud-platform','https://www.googleapis.com/auth/sqlservice.admin'],
        metadata={'enable-cloud-sql-hive-metastore':'false','additional-cloud-sql-instances':'modern-heading-234419:us-central1:sklearndata-1'},
        region='us-central1',
        zone=models.Variable.get('gce_zone'),
        master_machine_type='n1-standard-1',
        worker_machine_type='n1-standard-1')


    copy_steps = bash_operator.BashOperator(
        task_id='start',
        bash_command='gsutil cp gs://heading-234419-sklearn_poc/steps-end-to-end.sh /home/airflow/gcs/data/')

    copy_steps_for_version = bash_operator.BashOperator(
        task_id='start1',
        bash_command='gsutil cp gs://heading-234419-sklearn_poc/pyspark.sh /home/airflow/gcs/data/')
    # [END composer_simple_operators]
	# Likewise, the goodbye_bash task calls a Bash script.
    init = bash_operator.BashOperator(
        task_id='initialization',
        bash_command=dep_command)

    version_step = bash_operator.BashOperator(
            task_id='initialization1',
            bash_command=dep_command_1)
    # [END composer_simple_operators]
    # Likewise, the goodbye_bash task calls a Bash script.

    # [END composer_simple_operators]

	 # Likewise, the goodbye_bash task calls a Bash script.
    model_dev = bash_operator.BashOperator(
        task_id='model_dev',
        bash_command='python /home/airflow/gcs/data/demo_2_model_dev.py')
    # [END composer_simple_operators]

	 # Likewise, the goodbye_bash task calls a Bash script.
    model_deploy = bash_operator.BashOperator(
        task_id='model_deploy',
        bash_command='python /home/airflow/gcs/data/demo_2_deployment.py')
    # [END composer_simple_operators]

    submit_job = dataproc_operator.DataProcPySparkOperator(
        task_id='data_clean',
        main=pysparkFile,
        cluster_name='spark-data-cluster-{{ ds_nodash }}',
        job_name='spak-data-job',
        region='us-central1')

    delete_dataproc_cluster = dataproc_operator.DataprocClusterDeleteOperator(
        task_id='delete_dataproc_cluster',
        cluster_name='spark-data-cluster-{{ ds_nodash }}',
        # Setting trigger_rule to ALL_DONE causes the cluster to be deleted
        # even if the Dataproc job fails.
        region='us-central1',
        trigger_rule=trigger_rule.TriggerRule.ALL_DONE)

    # [START composer_simple_relationships]
    # Define the order in which the tasks complete by using the >> and <<
    # operators. In this example, hello_python executes before goodbye_bash.
    # create_dataproc_cluster >> submit_job >> delete_dataproc_cluster >>
    copy_steps >> init >> copy_steps_for_version >> model_dev >> version_step >>  model_deploy
    # [END composer_simple_relationships]
# [END composer_simple]
