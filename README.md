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
sudo pip install Fabric fabtools
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


Schema
------
The following table shows how the internal architecture of myChef works, with their ports and configuration files

Tool          | Description                                                             | configuration file         | ports
------------- | ----------------------------------------------------------------------  | -------------------------- | -----
Graphite      | Graphic tool for showing the signals of Statsd                          | /opt/graphite/conf         | 2003 (Carbon)
Statsd        | framework for making aggregation with the signals of our application    | /opt/statsd/localConfig.js | 8125
Grafana       | Improved dashboard for Graphite                                         | /opt/grafana/              | 8080 (grafana.vagrant.com:8080)
Elasticsearch | Indexing engine for searching our logs                                  |                            | 9200 (HTTP)
Logstash      | Tool for reading, parsing, processing and sending logs to Elasticsearch | /etc/logstash/conf.d       | It depends of the configuration (currently 5858 for UDP)
Kibana        | Web interface for logstash/elasticsearch data                           | /opt/kibana/config.js      | 8080 (kibana.vagrant.com:8080)

[Vagrant main page]:http://www.vagrantup.com/
[PIP download page]:http://pip.readthedocs.org/en/latest/installing.html
