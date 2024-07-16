resource "google_container_cluster" "cluster1" {
  name               = "cluster-asia"
  location           = "${var.subnets[0].region}-a" // specify zone instead of region
  initial_node_count = 1


  node_config {
    machine_type = "e2-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-standard"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }

  network    = google_compute_network.vikraya_network.self_link
  subnetwork = google_compute_subnetwork.subnet[0].name
  gateway_api_config {
    channel="CHANNEL_STANDARD"
  }
  addons_config {
    http_load_balancing {
      disabled = false
    }
   workload_identity_config {
   workload_pool = "${var.PROJECT_ID}.svc.id.goog"
   }

    horizontal_pod_autoscaling {
      disabled = false
    }

    network_policy_config {
      disabled = true
    }


  }

}

resource "google_container_cluster" "cluster2" {
  name               = "cluster-us"
  location           = "${var.subnets[1].region}-a" // specify zone instead of region
  initial_node_count = 1



  node_config {
    machine_type = "e2-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-standard"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }

  network    = google_compute_network.vikraya_network.self_link
  subnetwork = google_compute_subnetwork.subnet[1].name
  
   workload_identity_config {
   workload_pool = "${var.PROJECT_ID}.svc.id.goog"
   }
  addons_config {
    http_load_balancing {
      disabled = false
    }

    horizontal_pod_autoscaling {
      disabled = false
    }

    network_policy_config {
      disabled = true
    }


  }
}
