Vagrant.configure(2) do |config|
  config.vm.box = "williamyeh/ubuntu-trusty64-docker"

  config.vm.network "forwarded_port", guest: 9090, host: 9090

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "deploy/ansible/test_env.yml"
    ansible.verbose = "vv"
  end
end