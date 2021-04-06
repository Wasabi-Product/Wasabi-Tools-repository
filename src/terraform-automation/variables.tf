# region for aws and minio
variable "region" {
  description = "Default region"
  default = "us-east-1"
}

# server location for local minio server
variable "minio_server" {
  description = "Default MINIO host and port"
  default = "localhost:9000"
}

# access key
variable "access_key" {
  description = "User"
  default = "<access key>"
}

# secret key
variable "secret_key" {
  description = "Secret user"
  default = "<secret key>"
}

# prefix appended to bucket name and policy
variable "name-addon" {
  type = string
  description = "a prefix added to the usernames"
  default = "wasabi-technologies-"
}

# list of usernames to be added to the group
variable "usernames" {
  description = "usernames to be created on Wasabi"
  default = ["<usernames here>"]
}

# group name.
variable "group-name" {
  description = "name of the group users will be added to."
  default = "restricted-access-group"
}
