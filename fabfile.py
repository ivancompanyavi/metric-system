#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from vagrant import vagrant
from fabric.api import cd, sudo, run, put, settings, task
from fabric.operations import prompt
from fabric.contrib.files import exists
import getpass
import pkg_resources


def config_file(folder, filepath):
    return pkg_resources.resource_filename(__name__,
                                           '/config/{0}/{1}'.format(folder, filepath))

def command_exists(command):
    """
    Checks if the command 'command' exists
    """
    result = False
    with settings(warn_only=True):
        checked = run('command -v %s' % command)
        if checked.return_code == 0:
            result = True

    return result

def install_wget():
    if not command_exists('wget'):
        sudo('yum install -y wget')

def _install_python():
    install_wget()
    if not command_exists('python2.7'):
        run('mkdir -p /home/vagrant/src')
        with cd('/home/vagrant/src'):
            run('wget --no-check-certificate https://www.python.org/ftp/python/2.7.7/Python-2.7.7.tar.xz')
            run('tar xf Python-2.7.7.tar.xz')
        with cd('/home/vagrant/src/Python-2.7.7'):
            sudo('./configure --prefix=/usr')
            sudo('make && make altinstall')
        with cd('/home/vagrant'):
            run('echo "alias python=/usr/bin/python2.7" >> .bashrc')
            run('source .bashrc')


def _install_pip():
    run('mkdir -p /home/vagrant/src')
    sudo('yum install -y zlib-devel openssl-devel curses-devel')
    _install_python()
    install_wget()
    if not command_exists('pip'):
        with cd('/home/vagrant/src'):
            run('wget https://bootstrap.pypa.io/ez_setup.py')
            sudo('/usr/bin/python2.7 ez_setup.py')
            run('wget https://bootstrap.pypa.io/get-pip.py')
            sudo('/usr/bin/python2.7 get-pip.py')


def _install_nginx():
    run('mkdir -p /home/vagrant/src')
    install_wget()

    # Downloading PCRE source (Required for nginx)
    with cd('/home/vagrant/src'):
        run('wget http://sourceforge.net/projects/pcre/files/pcre/8.33/pcre-8.33.tar.gz/download# -O pcre-8.33.tar.gz')
        run('tar -zxvf pcre-8.33.tar.gz')

    # creating nginx etc and log folders
    sudo('mkdir -p /etc/nginx')
    sudo('mkdir -p /var/log/nginx')
    sudo('chmod 777 -R /etc/nginx')
    sudo('chmod 777 -R /var/log/nginx')
    sudo('chown -R vagrant: /var/log/nginx')

    # downloading nginx source
    with cd('/home/vagrant/src'):
        run('wget http://nginx.org/download/nginx-1.2.7.tar.gz')
        run('tar -zxvf nginx-1.2.7.tar.gz')

    # installing nginx
    with cd('/home/vagrant/src/nginx-1.2.7'):
        sudo('./configure --prefix=/usr --with-pcre=/home/vagrant/src/pcre-8.33/ --with-http_ssl_module --with-http_gzip_static_module --conf-path=/etc/nginx/nginx.conf --pid-path=/var/run/nginx.pid --lock-path=/var/lock/nginx.lock --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --user=vagrant --group=vagrant')
        sudo('make && make install')

    put(config_file('graphite', 'nginx.conf'), '/etc/nginx/', use_sudo=True)
    put(config_file('graphite', 'nginx'), '/etc/init.d/', use_sudo=True)
    sudo('chmod ugo+x /etc/init.d/nginx')
    sudo('chkconfig nginx on')

    # starting nginx
    sudo('nginx')


@task
def install_graphite():
    """
    Installs Graphite and dependencies
    """
    sudo('yum -y upgrade')
    sudo('yum -y install gcc libffi-devel wget python-devel bzip2-devel sqlite-devel libpng-devel pixman pixman-devel cairo pycairo')
    run('mkdir -p /home/vagrant/src')
    _install_pip()
    sudo('pip install supervisor simplejson cairocffi') # required for django admin
    sudo('mkdir -p /opt/graphite')
    sudo('chmod 777 -R /opt')
    sudo('pip install git+https://github.com/graphite-project/carbon.git@0.9.x#egg=carbon')
    sudo('pip install git+https://github.com/graphite-project/whisper.git@master#egg=whisper')
    sudo('pip install django==1.5.2 django-tagging uwsgi')
    sudo('pip install git+https://github.com/graphite-project/graphite-web.git@0.9.x#egg=graphite-web')

    # creating automatic startup scripts for nginx and carbon
    put(config_file('graphite', 'carbon'), '/etc/init.d/', use_sudo=True)
    
    sudo('chmod ugo+x /etc/init.d/carbon')
    put(config_file('graphite', 'glyph.py'), '/opt/graphite/webapp/graphite/render', use_sudo=True)
    
    sudo('chkconfig carbon on')

    # copying nginx and uwsgi configuration files
    sudo('mkdir -p /etc/supervisor/conf.d/')
    sudo('mkdir -p /var/log/uwsgi')
    sudo('chmod 777 -R /var/log/uwsgi')
    sudo('chown -R vagrant: /var/log/uwsgi')
    put(config_file('graphite', 'supervisord.conf'), '/etc/supervisord.conf', use_sudo=True)
    put(config_file('graphite', 'uwsgi.conf'), '/etc/supervisor/conf.d/', use_sudo=True)
    
    
    sudo('echo "/usr/lib" > /etc/ld.so.conf.d/pycairo.conf')
    sudo('ldconfig')
    # setting the carbon config files (default)
    with cd('/opt/graphite/conf/'):
        sudo('cp carbon.conf.example carbon.conf')
        put(config_file('graphite', 'storage-schemas.conf'), 'storage-schemas.conf', use_sudo=True)
    # clearing old carbon log files
    put(config_file('graphite', 'carbon-logrotate'), '/etc/cron.daily/', use_sudo=True, mode=0755)

    # initializing graphite django db
    with cd('/opt/graphite/webapp/graphite'):
        sudo("/usr/bin/python2.7 manage.py syncdb")

    # changing ownership on graphite folders
    sudo('chown -R vagrant: /opt/graphite/')

    # starting uwsgi

    run('supervisord')
    run('supervisorctl update && supervisorctl restart uwsgi')

    # starting carbon-cache
    sudo('/etc/init.d/carbon start')

    _install_nginx()


"""
 ===========================
    Statsd installation
 ===========================
"""
@task
def install_statsd():
    """
    Installs etsy's node.js statsd and dependencies
    """
    sudo('yum install -y wget build-essential supervisor make git-core')
    with cd('/home/vagrant/src'):
        run('wget -N http://nodejs.org/dist/node-latest.tar.gz')
        run('tar -zxvf node-latest.tar.gz')
        sudo('cd `ls -rd node-v*` && make install')

    with cd('/opt'):
        run('git clone https://github.com/etsy/statsd.git')

    with cd('/opt/statsd'):
        run('git checkout v0.7.1') # or comment this out and stay on trunk
        put(config_file('statsd', 'localConfig.js'), 'localConfig.js', use_sudo=True)
        run('npm install')
    put(config_file('statsd', 'statsd.conf'), '/etc/supervisor/conf.d/', use_sudo=True)
    sudo('supervisorctl update && supervisorctl start statsd')

    # UDP buffer tuning for statsd
    sudo('mkdir -p /etc/sysctl.d')
    put(config_file('statsd', '10-statsd.conf'), '/etc/sysctl.d/', use_sudo=True)
    sudo('sysctl -p /etc/sysctl.d/10-statsd.conf')

"""
 ===========================
    Grafana installation
 ===========================
"""

@task
def install_grafana():
    """
    Installs Grafana
    """
    with cd('/home/vagrant/src'):
        run('wget http://grafanarel.s3.amazonaws.com/grafana-1.6.0.tar.gz')
        run('tar -xzvf grafana-1.6.0.tar.gz')
        sudo('mv grafana-1.6.0/ /opt/grafana')
    with cd('/opt/grafana'):
        put(config_file('grafana', 'config.js'), 'config.js', use_sudo=True)

    sudo('nginx -s reload')



@task
def install_elasticsearch():
    sudo('yum install -y java-1.7.0-openjdk java-1.7.0-openjdk-devel')
    sudo('rpm --import http://packages.elasticsearch.org/GPG-KEY-elasticsearch')
    put(config_file('elasticsearch', 'elasticsearch.repo'), '/etc/yum.repos.d/', use_sudo=True)
    sudo('yum install -y elasticsearch')
    sudo('service elasticsearch start')

@task
def install_logstash():
    sudo('rpm --import http://packages.elasticsearch.org/GPG-KEY-elasticsearch')
    put(config_file('logstash', 'logstash.repo'), '/etc/yum.repos.d/', use_sudo=True)
    sudo('yum install -y logstash')
    put(config_file('logstash', 'scraper.conf'), '/etc/logstash/conf.d', use_sudo=True)
    sudo('service logstash start')

@task
def install_kibana():
    with cd('/home/vagrant/src'):
        run('wget https://download.elasticsearch.org/kibana/kibana/kibana-3.1.0.tar.gz')
        run('tar -xzvf kibana-3.1.0.tar.gz')
        sudo('mv kibana-3.1.0 /opt/kibana')


@task
def install():
    #install_graphite()
    #install_statsd()
    #install_grafana()
    install_elasticsearch()
    install_logstash()
    install_kibana()