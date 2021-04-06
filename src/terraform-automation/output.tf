output "secret" {
  value = tomap({
  for k, s in aws_iam_access_key.iam_user_keys : k => [
    s.id,
    s.secret]
  })
}