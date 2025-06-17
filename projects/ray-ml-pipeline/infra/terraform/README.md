# Terraform IAM Starter Kit for Ray ML Pipeline

This folder sets up basic IAM for `ml_engineer` to access EKS, EC2, Lambda, and CloudWatch.

## Structure

- `main.tf`: Core IAM setup
- `ml_engineer_policy.json`: JSON policy document
- `outputs.tf`: Outputs AWS access keys
- `variables.tf`: Terraform variables
- `env/`: Contains environment-specific variable files
- `Makefile`: Easy commands to run Terraform

## Usage

```bash
make init
make plan
make apply
make output
```

Ensure your AWS credentials are available (via `aws configure` or environment variables).

To destroy the setup:

```bash
make destroy
```

Customize `env/dev.tfvars` to suit your AWS region or other config needs.
