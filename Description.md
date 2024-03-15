# Vikraya: Your Online Shopping Destination

Vikraya is an online shopping platform composed of various microservices built on Google Cloud Platform. It aims to provide a seamless shopping experience by integrating various services and technologies.

## Microservices

* **Frontend:** Serves UI to the user and sends requests to other backend microservices for data.
* **Auth-service:** Manages user authentication and registration. It uses Firestore database to store user info.
* **Cart-service:** Manages the products added to the cart by the user. It uses Firestore database to store cart info.
* **Catalog-service:** Retrieves products from the catalog by categories or all or by search. All products info is stored in Firestore database.
* **Order-service:** Manages user orders like cancelling or creating orders or showing orders of a user. It uses Firestore database to store order info.

## Infrastructure

The microservices are deployed on two Google Kubernetes Engine clusters which are registered to the same GKE fleet to enable multi-cluster deployment. All services are served by a multi-cluster gateway.

## Monitoring and Logging

Cloud Logging is used to log the info to know what happens in the system. Prometheus is used for cloud monitoring and dashboards are created in Google Cloud Monitoring. Synthetic monitoring is also set up for checking the uptime of the frontend service.

## Session Management

A Redis instance is created for saving user info which ensures distributed session management. This avoids the usage of sticky session affinities and stores session in a central Redis instance.

## Search Service

A Cloud Run service is deployed which uses RAG from GenAI and performs vector search on product description and product name embeddings to get related images. This service is served by a Google Cloud API Gateway secured with an API key.

## Deployment

Helm, the Kubernetes package manager, is used for deploying the services.

## Data Collection

Web scraping with Python is used to collect all the product info by scraping a website named JackJones.

## Image Storage

Google Cloud Storage bucket is used to store all images and it is made public.