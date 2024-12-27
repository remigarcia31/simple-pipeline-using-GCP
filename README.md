# Simple Pipeline Using GCP

Ce projet est un tutoriel démontrant comment créer une pipeline de données en utilisant Docker, Airflow, Terraform et Google Cloud Platform (GCP). L'objectif est de fournir une introduction pratique à la création de pipelines de données sur GCP.

## Table des matières

- [Aperçu](#aperçu)
- [Prérequis](#prérequis)
- [Architecture](#architecture)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Nettoyage](#nettoyage)
- [Ressources supplémentaires](#ressources-supplémentaires)


## Aperçu

Ce projet configure une pipeline de données simple qui :

1. **Ingestion** : Charge des données depuis une source spécifiée.
2. **Traitement** : Traite les données en utilisant des tâches définies dans Airflow.
3. **Stockage** : Stocke les données traitées dans une destination sur GCP, telle que BigQuery.


## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Terraform](https://www.terraform.io/)
- Un compte Google Cloud Platform avec les autorisations appropriées
- [gcloud CLI](https://cloud.google.com/sdk/gcloud)

Ne vous inquiétez pas nous allons tout faire petit à petit

## Architecture

L'architecture de la pipeline repose sur les éléments suivants :

1. **Docker** : Conteneurise les services pour assurer la portabilité et la cohérence des environnements.
2. **Airflow** : Orchestration des tâches de la pipeline.
3. **Terraform** : Provisionnement de l'infrastructure sur GCP.
4. **GCP Services** : Utilisation de services tels que Cloud Storage et BigQuery pour le stockage et le traitement des données.


## Installation

### 1. Cloner le dépôt

Commencez par cloner ce dépôt sur votre machine locale et naviguez dans le répertoire du projet :

```bash
git clone https://github.com/remigarcia31/simple-pipeline-using-GCP.git
cd simple-pipeline-using-GCP
```

### 2. Configurer les variables d'environnement

Nous allons créer compte de service :
  1. Allez sur IAM et administration
  2. Cliquez sur "Créer un compte de service"
     ***insérer image***
  4. Mettez les droits pour Administrateur BigQuery - Administrateur des objets Storage - Administrateur Storage
     ***insérer image***

//todo : AJOUTER LES ETAPES POUR GÉNÉRER LE CREDENTIALS

Créez un fichier .env à la racine du projet et définissez les variables nécessaires pour votre configuration GCP.
Prenez exemple sur le .env_example que j'ai mis sur le repo, modifiez avec vos données.

### 3. Initialiser Terraform

//todo : AJOUTER LES ETAPES POUR PRÉPARER LES VARIABLES TERRAFORMS

Naviguez dans le répertoire Terraform et initialisez l'environnement Terraform :

```bash
cd terraform
terraform init
```

### 4. Appliquer la configuration Terraform
Appliquez la configuration pour provisionner l'infrastructure GCP :


```bash
terraform apply
```
Confirmez l'opération en tapant yes lorsque Terraform vous le demande.

### 5. Démarrer les services Docker
Une fois l'infrastructure GCP en place, démarrez les services Docker pour exécuter Airflow :

```bash
cd ../airflow
docker-compose up -d
```
Airflow sera disponible à l'adresse http://localhost:8080.

## Utilisation

### 1. Accéder à l'interface Airflow
Ouvrez un navigateur et accédez à l'interface utilisateur d'Airflow à l'adresse :

http://localhost:8080

Utilisez les identifiants par défaut pour vous connecter :
- Nom d'utilisateur : airflow
- Mot de passe : airflow


### 2. Déclencher la pipeline
Dans l'interface Airflow :

Activez le DAG correspondant à votre pipeline.
Exécutez le DAG manuellement pour déclencher le processus.
Ce DAG ingérera les données, les traitera et les stockera dans BigQuery.

## Nettoyage
###1. Arrêter les services Docker
Pour arrêter les services Docker, exécutez :


```bash
cd ../airflow
docker-compose down
```

### 2. Détruire l'infrastructure Terraform
Pour supprimer toutes les ressources provisionnées sur GCP, naviguez dans le répertoire Terraform et exécutez :

```bash
cd ../terraform
terraform destroy
```
Confirmez l'opération en tapant yes.

## Ressources supplémentaires
Pour en savoir plus sur les outils utilisés dans ce projet :

- Documentation Docker
- Documentation Airflow
- Documentation Terraform
- Documentation GCP
