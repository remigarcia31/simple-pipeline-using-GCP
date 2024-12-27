variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my-creds.json"
  #ex : si vous avez un répertoire contenant ce fichier appelé "keys" avec votre fichier JSON de compte de service
  #sauvegardé sous le nom my-creds.json vous pouvez utiliser default = "./keys/my-creds.json"
}

variable "project" {
  description = "Projet"
  default     = "nom_du_projet_gcp"
}

variable "region" {
  description = "Région"
  #Mettez à jour ci-dessous avec la région souhaitée
  default = "europe-west1"
}

variable "location" {
  description = "Localisation du Projet"
  #Mettez à jour ci-dessous avec la localisation souhaitée
  default = "EU"
}

variable "bq_dataset_name" {
  description = "Nom de Mon Dataset BigQuery"
  #Mettez à jour ci-dessous avec le nom que vous souhaitez donner à votre dataset
  default = "nom_dataset_bigquery"
}

variable "gcs_bucket_name" {
  description = "Nom de Mon Bucket de Stockage"
  #Mettez à jour ci-dessous avec un nom unique pour votre bucket
  default = "nom_du_bucket"
}

variable "gcs_storage_class" {
  description = "Classe de Stockage du Bucket"
  default     = "STANDARD"
}