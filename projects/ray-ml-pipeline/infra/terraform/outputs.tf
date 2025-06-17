output "ml_engineer_access_key_id" {
  value = aws_iam_access_key.ml_engineer_key.id
}

output "ml_engineer_secret_access_key" {
  value     = aws_iam_access_key.ml_engineer_key.secret
  sensitive = true
}
