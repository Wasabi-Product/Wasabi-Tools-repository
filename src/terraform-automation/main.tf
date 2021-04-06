# Plugin required to create buckets through minio.
terraform {
  required_providers {
    minio = {
      source = "aminueza/minio"
      version = ">= 1.0.0"
    }
  }
  required_version = ">= 0.13"
}

# AWS provider to connect sts, iam and s3
provider aws {
  alias = "wasabi"
  region = var.region

  #coded credentials from variables file
  access_key = var.access_key
  secret_key = var.secret_key

  endpoints {
    sts = "https://sts.wasabisys.com"
    iam = "https://iam.wasabisys.com"
    s3 = "https://s3.wasabisys.com"
  }

  # skip checks
  s3_force_path_style = true
  skip_get_ec2_platforms = true
  skip_credentials_validation = true
  skip_metadata_api_check = true
  skip_requesting_account_id = true
}

# minio provider for creating buckets.
provider "minio" {
  minio_server = var.minio_server
  minio_region = var.region
  minio_access_key = var.access_key
  minio_secret_key = var.secret_key
}

