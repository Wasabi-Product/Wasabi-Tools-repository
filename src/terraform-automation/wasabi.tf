# 1. create IAM users based on the variables list
resource "aws_iam_user" "iam_users" {
  for_each = toset(var.usernames)
  name = each.key
  provider = aws.wasabi
  force_destroy = true
}

# 2. create access key for created user
resource "aws_iam_access_key" "iam_user_keys" {
  for_each = aws_iam_user.iam_users
  user = each.key
  provider = aws.wasabi
  depends_on = [
    aws_iam_user.iam_users]
}

# 3. Create buckets
resource "minio_s3_bucket" "bucket" {
  for_each = toset(var.usernames)
  bucket = format("%s%s", var.name-addon, each.key)
  acl = "private"
}

# 4. Create Group
resource "aws_iam_group" "restricted_access_group" {
  name = var.group-name
  provider = aws.wasabi
}

# 5. Create Policy
resource "aws_iam_policy" "restricted_access_policy" {
  name = "restricted-access-policy"

  policy = jsonencode(
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        Effect: "Allow",
        Action: "s3:ListAllMyBuckets",
        Resource: "arn:aws:s3:::*"
      },
      {
        Effect: "Allow",
        Action: "s3:*",
        Resource: [
          "arn:aws:s3:::wasabi-technologies-$${aws:username}",
          # Change wasabi-technologies- to something else if you change the variables.tf file.
          "arn:aws:s3:::wasabi-technologies-$${aws:username}/*"
          # Change wasabi-technologies- to something else if you change the variables.tf file.
        ]
      }
    ]
  }
  )
  provider = aws.wasabi
}

# 6. Attach policy to group
resource "aws_iam_policy_attachment" "test-attach" {
  name = "test-attachment"
  groups = [
    aws_iam_group.restricted_access_group.name]
  policy_arn = aws_iam_policy.restricted_access_policy.arn
  provider = aws.wasabi
  depends_on = [
    aws_iam_policy.restricted_access_policy,
    aws_iam_group.restricted_access_group]
}

# 7. Attach user to group
resource "aws_iam_group_membership" "add_users_to_group" {
  name = "tf-group-membership"
  for_each = aws_iam_user.iam_users
  users = var.usernames
  group = aws_iam_group.restricted_access_group.name
  provider = aws.wasabi
  depends_on = [
    aws_iam_group.restricted_access_group,
    aws_iam_user.iam_users]
}