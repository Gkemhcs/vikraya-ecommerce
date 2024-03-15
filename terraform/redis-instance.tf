

resource "google_compute_global_address" "private_ip_address" {
  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vikraya_network.self_link
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vikraya_network.self_link
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

resource "google_redis_instance" "basic_redis" {
  name           = "basic-redis"
  memory_size_gb = 1
  region         = "asia-south2"

  redis_configs = {
    "notify-keyspace-events" = "E"
  }

  auth_enabled = true

  transit_encryption_mode = "DISABLED"

  connect_mode = "PRIVATE_SERVICE_ACCESS"

  authorized_network = google_compute_network.vikraya_network.self_link
}
