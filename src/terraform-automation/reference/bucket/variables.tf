variable "minio_region" {
  description = "Default MINIO region"
  default     = "us-east-1"
}

variable "minio_server" {
  description = "Default MINIO host and port"
  default = "localhost:9000"
}

variable "minio_access_key" {
  description = "MINIO user"
  default = "IZQ5DQ9A4FM3B3PGKDLK"
}

variable "minio_secret_key" {
  description = "MINIO secret user"
  default = "EoceSQHpoa6rtrAXAi0SC0pW0ectLfgW3BQeJVV7"
}