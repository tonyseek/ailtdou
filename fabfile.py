from fabric.api import cd, run, sudo, hosts
from fabric.context_managers import prefix


remote_host = 'szulabs.org'
remote_repo = '/srv/ailtdou.szulabs.org'
remote_user = 'ailtdou'
remote_proc = 'ailtdou:*'

python_init = 'eval "$(pyenv init -)"'
honcho_init = 'honcho -e production/.env run '


@hosts(remote_host)
def deploy():
    with cd(remote_repo):
        sudo('git pull --ff-only origin master', user=remote_user)
        run('pip install -r requirements.txt')
        with prefix(python_init):
            sudo(honcho_init + 'python manage.py clean', user=remote_user)
            sudo(honcho_init + 'python manage.py db upgrade', user=remote_user)
    sudo('supervisorctl restart %s' % remote_proc)
