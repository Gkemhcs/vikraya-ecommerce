
resource "google_service_account" "vector_search_api" {
  account_id   = "vector-search-api"
  display_name = "vector-search-api"
  project      = var.PROJECT_ID
}

resource "google_project_iam_member" "aiplatform_user" {
  project = var.PROJECT_ID
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.vector_search_api.email}"
}

resource "google_cloud_run_service" "vector_search_api_service" {
  name     = "vector-search-api-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = var.VECTOR_SEARCH_API_IMAGE
      }
      service_account_name = google_service_account.vector_search_api.email
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  autogenerate_revision_name = true
}

resource "google_cloud_run_service_iam_member" "vector_search_api_service_invoker" {
  service  = google_cloud_run_service.vector_search_api_service.name
  location = "us-central1"
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.gateway_api.email}"
}