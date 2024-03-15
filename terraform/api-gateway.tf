locals {
  openapi = templatefile("${path.module}/openapi.yaml.tpl", {
    cloud_run_service_url = google_cloud_run_service.vector_search_api_service.status[0].url
  })
}

resource "google_service_account" "gateway_api" {

  account_id   = "gateway-api"
  display_name = "gateway-api"
  project      = var.PROJECT_ID
}

resource "google_api_gateway_api" "api" {
  provider = google-beta
  api_id   = "my-api"
  project  = var.PROJECT_ID
}


resource "google_api_gateway_api_config" "api_config" {
  provider      = google-beta
  api           = google_api_gateway_api.api.api_id
  api_config_id = "api-config"
  project       = var.PROJECT_ID

  openapi_documents {
    document {
      path     = "openapi.yaml"
     contents = base64encode(local.openapi)
    }
  }

  gateway_config {
    backend_config {
      google_service_account = google_service_account.gateway_api.email
    }
  }

  depends_on = [google_cloud_run_service.vector_search_api_service]

}

resource "google_api_gateway_gateway" "gateway" {
  provider   = google-beta
  gateway_id = "my-gateway"

  api_config = google_api_gateway_api_config.api_config.id
  project    = var.PROJECT_ID
  region     = "us-central1"
  labels = {
    env = "prod"
  }
  depends_on = [google_api_gateway_api_config.api_config]
}