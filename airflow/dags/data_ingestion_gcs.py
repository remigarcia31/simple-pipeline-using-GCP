import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException  # Ajout de l'import manquant

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq

# Récupérer les variables d'environnement
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCS_BUCKET_NAME")
path_to_local_home = os.environ.get("AIRFLOW_HOME")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET")

dataset_name = "JO_2024_spectateurs.parquet"
dataset_url = f"https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/paris-2024-psa-snm/exports/parquet"


def verify_parquet_file(file_path):
    """
    Vérifie si le fichier est un Parquet valide.
    Lève une exception si le fichier n'est pas un Parquet valide.
    """
    try:
        # Vérifie d'abord si le fichier existe
        if not os.path.exists(file_path):
            raise AirflowException(f"Le fichier {file_path} n'existe pas")
            
        # Vérifie la taille du fichier
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise AirflowException(f"Le fichier {file_path} est vide")
            
        # Tente de lire le fichier Parquet
        table = pq.read_table(file_path)
        logging.info(f"Le fichier {file_path} est un Parquet valide")
        logging.info(f"Schéma du fichier: {table.schema}")
        logging.info(f"Nombre de lignes: {table.num_rows}")
        return True
    except Exception as e:
        logging.error(f"Erreur lors de la vérification du fichier Parquet: {str(e)}")
        raise AirflowException(f"Le fichier n'est pas un Parquet valide: {str(e)}")

def upload_to_gcs(bucket, object_name, local_file):
    """
    Fonction pour télécharger un fichier vers un bucket GCS.
    """
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    logging.info(f"Téléversement dans le bucket : {bucket}, fichier : {local_file}")
    blob.upload_from_filename(local_file)

def check_service_account():
    """
    Vérifie et affiche quel service account est utilisé pour l'authentification.
    """
    service_account = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    logging.info(f"Service Account being used: {service_account}")
    return service_account

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="data_ingestion_gcs",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['tuto'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sS {dataset_url} > {path_to_local_home}/{dataset_name}"
    )

    verify_parquet_task = PythonOperator(
        task_id="verify_parquet_task",
        python_callable=verify_parquet_file,
        op_kwargs={
            "file_path": f"{path_to_local_home}/{dataset_name}",
        },
    )

    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{dataset_name}",
            "local_file": f"{path_to_local_home}/{dataset_name}",
        },
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_table",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/{dataset_name}"],
            },
        },
    )

    check_service_account_task = PythonOperator(
        task_id="check_service_account_task",
        python_callable=check_service_account,
    )

    download_dataset_task >> verify_parquet_task >> local_to_gcs_task >> bigquery_external_table_task
    download_dataset_task >> check_service_account_task