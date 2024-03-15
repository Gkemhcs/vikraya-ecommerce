subnets = [
  {
    name          = "subnet-asia"
    region        = "asia-south2"
    ip_cidr_range = "192.168.1.0/25"
    secondary_ranges = [
      {
        range_name    = "services"
        ip_cidr_range = "172.16.1.0/24"
      },
      {
        range_name    = "pods"
        ip_cidr_range = "172.16.2.0/24"
      }
    ]
  },
  {
    name          = "subnet-us"
    region        = "us-central1"
    ip_cidr_range = "192.168.2.0/25"
    secondary_ranges = [
      {
        range_name    = "services"
        ip_cidr_range = "172.16.3.0/24"
      },
      {
        range_name    = "pods"
        ip_cidr_range = "172.16.4.0/24"
      }
    ]
  }
]