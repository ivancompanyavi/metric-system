# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "centos"
  
  #Nginx
  config.vm.network :forwarded_port, guest: 8080, host: 8080
  config.vm.network :forwarded_port, guest: 443, host: 8443
  #Statsd
  config.vm.network :forwarded_port, guest: 8125, host: 8125
  #Scrapyd web interface
  config.vm.network :forwarded_port, guest: 6800, host: 6800
  config.vm.network :forwarded_port, guest: 9200, host: 9200
end
