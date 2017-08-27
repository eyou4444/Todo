from fabric.api import *

env.hosts = ['47.94.130.184']
env.user = 'root'
env.password = 'huxin@860404'


def hello():
    print 'hello world!'


def deploy():
    with cd('/root/Todo'):
        run('git pull')
        sudo('supervisorctl restart todo')
        sudo('supervisorctl status')
