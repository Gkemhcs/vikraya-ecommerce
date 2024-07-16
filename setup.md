# VIKRAYA   MULTI GKE CLUSTER ECOMMERCE MICROSERVICE
##  SETUP TO DEPLOY VIKRAYA IN YOUR GOOGLE CLOUD PROJECT
#####  Replace the PROJECT_ID  with your project_id
```bash
export PROJECT_ID="PROJECT_ID"

gcloud config set project $PROJECT_ID
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format "value(projectNumber)")
```

#### Enable required services 
``` bash 
gcloud services enable compute.googleapis.com container.googleapis.com \
  cloudbuild.googleapis.com  run.googleapis.com apigateway.googleapis.com aiplatform.googleapis.com \
  artifactregistry.googleapis.com cloudresourcemanager.googleapis.com datastore.googleapis.com firestore.googleapis.com \
  gkehub.googleapis.com  redis.googleapis.com servicenetworking.googleapis.com  servicecontrol.googleapis.com servicemanagement.googleapis.com  \
   multiclusterservicediscovery.googleapis.com multiclusteringress.googleapis.com trafficdirector.googleapis.com 

```
#### Now we need to create a service account for cloud build pipelines  instead of using compute engine-service-account

``` bash 
gcloud iam service-accounts create cloudbuild 
gcloud  projects add-iam-policy-binding vikraya-deployment --member "serviceAccount:cloudbuild@${PROJECT_ID}.iam.gserviceaccount.com" \
--role roles/logging.logWriter
gcloud  projects add-iam-policy-binding vikraya-deployment --member "serviceAccount:cloudbuild@${PROJECT_ID}.iam.gserviceaccount.com" \
--role roles/artifactregistry.createOnPushWriter
gcloud  projects add-iam-policy-binding vikraya-deployment --member "serviceAccount:cloudbuild@${PROJECT_ID}.iam.gserviceaccount.com" \
--role roles/storage.admin

```
#### Now we need to create an artifact registry to store the docker images of our microservices and vector search api
``` bash 
export ARTIFACT_REGISTRY_REPOSITORY_NAME="replace it with your  repo name "
gcloud artifacts repositories create  ${ARTIFACT_REGISTRY_REPOSITORY_NAME} \
--repository-format docker \
--location us \
--description "REPOSITORY TO STORE DOCKER IMAGES OF SERVICES OF VIKRAYA-ECOMMERCE"

gcloud config set artifacts/repository $ARTIFACT_REGISTRY_REPOSITORY_NAME 
gcloud config set artifacts/location us
```
#### Now we need to run the CLOUD-BUILD pipeline to create and store images of our microservices 
``` bash
gcloud  beta builds submit --config cloudbuild.yaml  \
--substitutions=_ARTIFACT_REGISTRY_REPOSITORY_LOCATION=us,_ARTIFACT_REGISTRY_REPOSITORY_NAME=${PROJECT_ID}
```
#### Create a GOOGLE_CLOUD_STORAGE_BUCKET to store the product images
``` bash 
read BUCKET_SUFFIX
export BUCKET_NAME=vikraya-ecommerce-${BUCKET_SUFFIX}
gsutil mb  -l us  gs://${BUCKET_NAME}
gsutil cp -r  static gs://${BUCKET_NAME}/app/
gsutil acl ch -u allUsers:R gs://${BUCKET_NAME}/app/**
 ```
#### Now we need to deploy our infrastructure using terraform


##### ALL THE CODE FOR TERRAFORM ARE IN terraform directory 
#### But before to deploy the infra first we need a terraform variables value named VECTOR_SEARCH_API_IMAGE
#####  Below command lists all docker images stored in our repository created previously  and from them copy the one which is having name containing vector-search
```bash 
gcloud artifacts docker images list 
```  
```bash
export VECTOR_SEARCH_API_IMAGE="REPLACE_IT_WITH_THE_CORRECT_IMAGE_YOU_HAVE_COPIED"
```
#### lets deploy the terraform 🕘
```bash 
cd terraform 
terraform init
terraform apply -auto-approve -var VECTOR_SEARCH_API_IMAGE=$VECTOR_SEARCH_API_IMAGE -var PROJECT_ID=$PROJECT_ID
echo "Infra deployed successfully ☑️"
export REDIS_INSTANCE_IP_ADDRESS=terraform output redis_ip
export API_GATEWAY_URL= "https://$(terraform output gateway_url)"
gcloud services enable $(gcloud api-gateway apis describe my-api  --format "value(managedService)")
cd ..
```
#### Now we need to populate the product_catalog collection in firestore database with the documents
``` bash
cd data-import
virtualenv venv
source venv/bin/activate
pip install google-cloud-firestore
sed -i "s/BUCKET_NAME/${BUCKET_NAME}/g" new-local-catalog.json 
python3 catalog_data_import.py
cd ..
```
#### NOW ITS TIME 🕐 TO DEPLOY OUR SERVICE MANIFESTS THROUGH HELM But before that we need to get some values and create service-account for our Values.yaml file 
```bash
echo "GETTING SOME REDIS  INSTANCE INFO"
export REDIS_HOST=$(gcloud redis instances describe basic-redis --region asia-south2 --format "value(host)")
export REDIS_PORT=$(gcloud redis instances describe basic-redis --region asia-south2 --format "value(port)")
export REDIS_AUTH_STRING=$(gcloud redis instances get-auth-string  basic-redis --region asia-south2 --format "value(authString)")
```
#### Here we are creating a service account for workload identity 
 ```bash 
gcloud iam service-accounts create firestore-user
gcloud  projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:firestore-user@${PROJECT_ID}.iam.gserviceaccount.com" \
--role roles/datastore.user
gcloud  projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:firestore-user@${PROJECT_ID}.iam.gserviceaccount.com" \
--role roles/logging.logWriter
export FIRESTORE_SERVICE_ACCOUNT=firestore-user@${PROJECT_ID}.iam.gserviceaccount.com
echo "adding some iam bindings for workload identity "
gcloud iam service-accounts add-iam-policy-binding  $FIRESTORE_SERVICE_ACCOUNT --member "serviceAccount:${PROJECT_ID}.svc.id.goog[auth-ns/auth-server-sa]" --role roles/iam.workloadIdentityUser
gcloud iam service-accounts add-iam-policy-binding  $FIRESTORE_SERVICE_ACCOUNT --member "serviceAccount:${PROJECT_ID}.svc.id.goog[cart-ns/cart-server-sa]" --role roles/iam.workloadIdentityUser
gcloud iam service-accounts add-iam-policy-binding  $FIRESTORE_SERVICE_ACCOUNT --member "serviceAccount:${PROJECT_ID}.svc.id.goog[catalog-ns/catalog-server-sa]" --role roles/iam.workloadIdentityUser
gcloud iam service-accounts add-iam-policy-binding  $FIRESTORE_SERVICE_ACCOUNT --member "serviceAccount:${PROJECT_ID}.svc.id.goog[order-ns/order-server-sa]" --role roles/iam.workloadIdentityUser
gcloud iam service-accounts add-iam-policy-binding  $FIRESTORE_SERVICE_ACCOUNT --member "serviceAccount:${PROJECT_ID}.svc.id.goog[frontend/frontend-sa]" --role roles/iam.workloadIdentityUser
```
#### GET AN API  KEY FROM GOOGLE CLOUD CONSOLE
```bash
export API_KEY="replace with your api key"
``` 

#### Now we need to replace the values in values.yaml with the values obtained from this project
```bash
sed -i  "s/GCP_SERVICE_ACCOUNT/${FIRESTORE_SERVICE_ACCOUNT}/" values.yaml 
sed -i "s/API_GATEWAY_URL/$(echo ${API_GATEWAY_URL}|tr -d '\n' |base64)/" values.yaml
sed -i "s/API_KEY/$(echo ${API_KEY}|tr -d '\n' |base64)/" values.yaml
sed -i "s/REDIS_SERVER_AUTH_STRING/$(echo ${REDIS_AUTH_STRING}|tr -d '\n' |base64)/" values.yaml
sed -i "s/REDIS_SERVER_IP_ADDRESS/$(echo ${REDIS_HOST}|tr -d '\n' |base64)/" values.yaml
sed -i "s/REDIS_SERVER_PORT/$(echo ${REDIS_PORT}|tr -d '\n' |base64)/" values.yaml
sed -i "s/PROJECT_ID/${PROJECT_ID}/" values.yaml
sed -i "s/ARTIFACT_REGISTRY_REPOSITORY/${ARTIFACT_REGISTRY_REPOSITORY_NAME}/" values.yaml
sed -i "s/ARTIFACT_REGISTRY_LOCATION/us/" values.yaml
```
#### Let's deploy the helm chart into clusters
```bash
helm install cluster-us vikraya-helm --values values.yaml
helm install cluster-asia vikraya-helm --values values.yaml --kube-context  cluster-asia
```
#### Register the gke clusters to fleet 
```bash
gcloud container fleet memberships register cluster-us --gke-cluster us-central1-a/cluster-us \
--enable-workload-identity
gcloud container fleet memberships register cluster-asia --gke-cluster asia-south2-a/cluster-asia \
--enable-workload-identity
```
### Enabling the multi cluster services and ingress 
```bash
gcloud container fleet multi-cluster-services enable \
    --project $PROJECT_ID
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:$PROJECT_ID.svc.id.goog[gke-mcs/gke-mcs-importer]" \
--role "roles/compute.networkViewer" \
--project=$PROJECT_ID
gcloud container fleet ingress enable \
--config-membership=projects/$PROJECT_ID/locations/asia-south2-a/memberships/cluster-asia \
--project=$PROJECT_ID    
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:service-$PROJECT_NUMBER@gcp-sa-multiclusteringress.iam.gserviceaccount.com" \
--role "roles/container.admin" \
--project=$PROJECT_ID
```
### Now deploy the multi cluster gateway into config cluster.Switch to config cluster using kubectl
```bash
kubectl apply -f kubernetes-templates/multi-cluster-gateway-templates/
```
### Now to access the  gateway ip  address
```bash
kubectl get  gateway frontend-global -n frontend
```
### Access the frontend by setting the header host to store.example.com and env to canary 





