from fabric.api import cd, run, get, put, sudo, hosts
from fabric.context_managers import prefix


remote_host = 'szulabs.org'
remote_repo = '/srv/ailtdou.szulabs.org'
remote_user = 'ailtdou'
remote_proc = 'ailtdou:*'

python_init = 'eval "$(pyenv init -)"'


@hosts(remote_host)
def sync():
    with cd(remote_repo):
        get('production/*.cfg', 'production/')


@hosts(remote_host)
def deploy():
    with cd(remote_repo):
        sudo('git pull --ff-only origin master', user=remote_user)
        run('pip install -r requirements.txt')
        get('production/*.cfg', 'production/%(basename)s.last')
        put('production/*.cfg', 'production/', use_sudo=True)
        with prefix(python_init), prefix('source production/.env'):
            sudo('python manage.py clean', user=remote_user)
            sudo('python manage.py db upgrade', user=remote_user)
    sudo('supervisorctl restart %s' % remote_proc)
