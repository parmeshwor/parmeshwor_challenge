terraform init
terraform plan
terraform apply

cd terraform
terraform output public_ip >> ../inventory.ini.template
cp ../inventory.ini.template ../ansible/inventory.ini

cd ../ansible
ansible-playbook p2.yml -i inventory.ini


