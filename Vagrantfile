# -*- mode: ruby -*-
# vi: set ft=ruby :

# PyBossa Vagrantfile

VAGRANTFILE_API_VERSION = "2"

require "vagrant-aws"

# Ansible install script for Ubuntu
$ansible_install_script = <<SCRIPT
export DEBIAN_FRONTEND=noninteractive
echo Check if Ansible existing...
if ! which ansible >/dev/null; then
  echo update package index files...
  apt-get update -qq
  echo install Ansible...
  apt-get install -qq ansible
fi
SCRIPT

$ansible_local_provisioning_script = <<SCRIPT
export DEBIAN_FRONTEND=noninteractive
export PYTHONUNBUFFERED=1
echo PyBossa provisioning with Ansible...
ansible-playbook -u vagrant /vagrant/provisioning/playbook.yml -i /vagrant/provisioning/ansible_hosts -c local
SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "aws-dummy"
  config.vm.provider "aws" do |aws, override|
    aws.instance_type = "t2.micro"
    aws.access_key_id = ENV["AWS_ACCESS_KEY_ID"]
    aws.secret_access_key = ENV["AWS_SECRET_ACCESS_KEY"]
    aws.keypair_name = "pybossa-admin"
    aws.region = "us-east-2"
    aws.ami = "ami-6a003c0f"
    aws.security_groups = ["pybossa"]
    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = "~/.ssh/pybossa-admin.pem"
  end
  # turn off warning message `stdin: is not a tty error`
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"
  # be sure that there  is Ansible for local provisioning
  config.vm.provision "shell", inline: $ansible_install_script
  # do the final Ansible local provisioning
  config.vm.provision "shell", inline: $ansible_local_provisioning_script
  config.vm.synced_folder ".", "/vagrant", disabled: false, type: 'rsync'
end
