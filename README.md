MyChef
======

MyChef is a boilerplate created for developing an environment in MyTaste with the tools needed for logging, searching and graphing.

Prerequisites
-------------
Before you start to download and play with the environment, you need to have the follow tools installed:

- Vagrant ([Vagrant main page])
- PIP ([Pip download page])
- Fabric and fabtools
```
pip install Fabric fabtools
```

Installation
------------
To install MyChef, follow these steps:
- Download this project
```
git clone https://github.com/ivangoblin/mychef.git
```
- Add the CentOS box to the Vagrant boxes
```
vagrant box add centos https://github.com/2creatives/vagrant-centos/releases/download/v6.5.3/centos65-x86_64-20140116.box
```
- Run the virtual machine
```
vagrant up
```
- Build the environment with fabric
```
fab vagrant install
```

[Vagrant main page]:http://www.vagrantup.com/
[PIP download page]:http://pip.readthedocs.org/en/latest/installing.html
