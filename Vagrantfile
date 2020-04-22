# -*- mode: ruby -*-
# vi: set ft=ruby :

INSTALL_TYPE    = ENV['VAGRANT_INSTALL_TYPE']   || 'local'                  # Options: local | docker

AMI_ID          = ENV['VAGRANT_AMI_ID']         || 'ami-02a599eb01e3b3c5b'  # Ubuntu 18.04 LTS @ ap-southeast-2
INSTANCE_TYPE   = ENV['VAGRANT_INSTANCE_TYPE']  || 'c5.large'
IAM_ROLE_NAME   = ENV['VAGARNT_IAM_ROLE']       || 'VagrantBaseEC2Role'
KEY_NAME        = ENV['VAGRANT_KEY_NAME']       || '<KEY_NAME_HERE>'
SG_NAME         = ENV['VAGRANT_SG_NAME']        || 'default'

APP_DATA_DIR    = ENV['VAGRANT_DATA_DIR']       || '/tmp/ramdisk'

Vagrant.configure('2') do |config|
  config.vm.box = 'dummy'

  config.vm.synced_folder '.', '/vagrant', type: 'rsync'

  config.vm.provider :aws do |aws, override|
    aws.ami = AMI_ID
    aws.instance_type = INSTANCE_TYPE
    aws.security_groups = [SG_NAME]
    aws.iam_instance_profile_name = IAM_ROLE_NAME
    aws.keypair_name = KEY_NAME

    override.ssh.username = 'ubuntu'
  end

  config.vm.provision 'shell', inline: <<-SHELL
    # Base
    apt-get update
    apt-get install -y htop vim git curl wget tree zip unzip
  SHELL

  if INSTALL_TYPE == 'docker'
    config.vm.provision 'shell', inline: <<-SHELL
      apt-get install -y docker.io
      usermod -a -G docker ubuntu
    SHELL
  else
    config.vm.provision 'shell', inline: <<-SHELL
      # Python
      apt-get install -y python3 python3-dev python3-pip
      pip3 install /vagrant/requirements.txt
      # App Deps
      mkdir #{APP_DATA_DIR}
      chown -R ubuntu. #{APP_DATA_DIR}
      mount -t tmpfs -o size=512M tmpfs #{APP_DATA_DIR}
    SHELL
  end
end
