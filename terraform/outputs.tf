output "redis_ip" {
  description = "The IP address of the Redis instance"
  value       = google_redis_instance.basic_redis.host
}
output  "gateway_url"{
  description = "THE URL OF API GATEWAY"
  value=google_api_gateway_gateway.gateway.default_hostname
}