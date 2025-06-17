provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_group" "ml_engineer" {
  name = "ml_engineer"
}

resource "aws_iam_policy" "ml_engineer_policy" {
  name        = "ml_engineer_policy"
  description = "Policy for ML Engineers to access EKS, EC2, Lambda, CloudWatch"
  policy      = file("ml_engineer_policy.json")
}

resource "aws_iam_group_policy_attachment" "ml_engineer_attach" {
  group      = aws_iam_group.ml_engineer.name
  policy_arn = aws_iam_policy.ml_engineer_policy.arn
}

resource "aws_iam_user" "ml_engineer_user" {
  name = "ml_engineer_user"
}

resource "aws_iam_user_group_membership" "ml_engineer_user_membership" {
  user   = aws_iam_user.ml_engineer_user.name
  groups = [aws_iam_group.ml_engineer.name]
}

resource "aws_iam_access_key" "ml_engineer_key" {
  user = aws_iam_user.ml_engineer_user.name
}
