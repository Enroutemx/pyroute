Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  ENV['LC_ALL']="en_US.UTF-8"
  config.ssh.username = 'ubuntu'
  config.vm.provision "shell", path: "configuration.sh"
  config.vm.network :forwarded_port, guest:4848, host:4848
  config.vm.network :private_network, ip: "10.0.0.10"
  config.vm.synced_folder ".", "/home/ubuntu/Pyroute"

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--cpuexecutioncap", "50", "--cpus", "1"]
    vb.memory = 1024
  end
end