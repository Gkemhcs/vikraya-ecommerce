# VIKRAYA   MULTI GKE CLUSTER ECOMMERCE MICROSERVICE

``` bash 
gcloud services enable compute.googleapis.com container.googleapis.com \
  cloudbuild.googleapis.com  run.googleapis.com apigateway.googleapis.com aiplatform.googleapis.com \
  artifactregistry.googleapis.com cloudresourcemanager.googleapis.com datastore.googleapis.com firestore.googleapis.com \
  gkehub.googleapis.com  redis.googleapis.com servicenetworking.googleapis.com  servicecontrol.googleapis.com servicemanagement.googleapis.com  \
   multiclusterservicediscovery.googleapis.com multiclusteringress.googleapis.com trafficdirector.googleapis.com 

```


``` bash 
gcloud iam service-accounts create cloudbuild 
gcloud  projects add-iam-policy-binding vikraya-deployment --member "serviceAccount:cloudbuild@${PROJECT_ID}.iam.gserviceaccount.com" \
--role roles/logging.logWriter
gcloud  projects add-iam-policy-binding vikraya-deployment --member "serviceAccount:cloudbuild@${PROJECT_ID}.iam.gserviceaccount.com" \
--role roles/artifactregistry.createOnPushWriter

```
``` bash 
export ARTIFACT_REGISTRY_REPOSITORY_NAME="replace it with your  repo name "
gcloud artifacts repositories create  ${ARTIFACT_REGISTRY_REPOSITORY_NAME} \
--repository-format docker \
--location us \
--description "REPOSITORY TO STORE DOCKER IMAGES OF SERVICES OF VIKRAYA-ECOMMERCE"

```

``` bash
gcloud  beta builds submit --config-file cloudbuild.yaml  \
--substitutions=_ARTIFACT_REGISTRY_REPOSITORY_LOCATION=us,_ARTIFACT_REGISTRY_REPOSITORY_NAME=${PROJECT_ID}
```

``` bash 
read BUCKET_SUFFIX
export BUCKET_NAME =vikraya-ecommerce-${BUCKET_SUFFIX}
gsutil mb  -l us  gs://${BUCKET_NAME}
gsutil cp -r  static gs:${BUCKET_NAME}/app/
gsutil acl ch -u allUsers:R gs://${BUCKET_NAME}/app/**
 ```