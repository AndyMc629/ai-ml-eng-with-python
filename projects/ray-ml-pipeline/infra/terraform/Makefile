AWS_PROFILE=ml_engineer
TF_DIR=.

init:
	cd $(TF_DIR) && terraform init

plan:
	cd $(TF_DIR) && terraform plan -var-file=env/dev.tfvars

apply:
	cd $(TF_DIR) && terraform apply -var-file=env/dev.tfvars

destroy:
	cd $(TF_DIR) && terraform destroy -var-file=env/dev.tfvars

output:
	cd $(TF_DIR) && terraform output
