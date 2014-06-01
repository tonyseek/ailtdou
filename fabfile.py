from fabric.api import cd, run, get, put, sudo, hosts


remote_host = 'szulabs.org'
remote_repo = '/srv/ailtdou.szulabs.org'
remote_user = 'ailtdou'
remote_proc = 'ailtdou:*'


@hosts(remote_host)
def sync():
    with cd(remote_repo):
        get('production/*.cfg', 'production/')


@hosts(remote_host)
def deploy():
    with cd(remote_repo):
        sudo('git pull --ff-only origin master', user=remote_user)
        run('pip install -r requirements.txt')
        get('production/*.cfg', 'production/%(basename)s.last.cfg')
        put('production/*.cfg', 'production/', use_sudo=True)
    sudo('supervisorctl restart %s' % remote_proc)