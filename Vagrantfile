Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end
  config.vm.network "forwarded_port", guest: 9090, host: 9090
  config.vm.network "forwarded_port", guest: 9087, host: 9087
  config.vm.network "forwarded_port", guest: 9088, host: 9088
  config.vm.network "forwarded_port", guest: 9089, host: 9089
  config.vm.network "forwarded_port", guest: 9091, host: 9091
  config.vm.network "forwarded_port", guest: 9092, host: 9092
  config.vm.network "forwarded_port", guest: 9086, host: 9086
  config.vm.network "forwarded_port", guest: 9085, host: 9085
  config.vm.network "forwarded_port", guest: 9093, host: 9093

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "deploy/ansible/test_env.yml"
    ansible.verbose = "vv"
  end
end