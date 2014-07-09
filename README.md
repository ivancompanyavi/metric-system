MyChef
======

MyChef is a boilerplate created for developing an environment in MyTaste with the tools needed for logging, searching and graphing. This environment builds the following tools:

- Graphite (Graphing tools)
- Grafana (An inproved dashboard for Graphite)
- Statsd (Tool for making aggregations and send them to the Graphite database)
- ElasticSearch (Searching and indexing system)
- Logstash (Logging system indexed with ElasticSearch)
- Kibana (Webapp to see the logs of Logstash)

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

Post-Installation
-----------------

In our new virtual environment we have started a NGINX server in order to have the two webapps up and running. If we want to see them, we have to add to our /etc/hosts the following lines:

```
127.0.0.1       graphite.vagrant.com
127.0.0.1       grafana.vagrant.com
127.0.0.1       kibana.vagrant.com
```

After this, you can access to Kibana and Grafana with http://kibana.vagrant.com:8080 and http://grafana.vagrant.com:8080

[Vagrant main page]:http://www.vagrantup.com/
[PIP download page]:http://pip.readthedocs.org/en/latest/installing.html
