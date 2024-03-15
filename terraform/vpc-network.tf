

resource "google_compute_network" "vikraya_network" {
  name                    = "vikraya-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  count              = length(var.subnets)
  name               = var.subnets[count.index].name
  region             = var.subnets[count.index].region
  ip_cidr_range      = var.subnets[count.index].ip_cidr_range
  network            = google_compute_network.vikraya_network.self_link
  secondary_ip_range = var.subnets[count.index].secondary_ranges
}