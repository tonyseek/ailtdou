from fabric.api import cd, run, sudo, hosts


remote_host = 'szulabs.org'
remote_repo = '/srv/ailtdou.szulabs.org'
remote_user = 'ailtdou'
remote_proc = ['ailtdou', 'ailtdou-smtp']
honcho_exec = 'pyenv exec honcho run '


@hosts(remote_host)
def deploy():
    with cd(remote_repo):
        sudo('git pull --ff-only origin master', user=remote_user)
        run('pip install -r requirements.txt')
        sudo(honcho_exec + 'python manage.py clean', user=remote_user)
        sudo(honcho_exec + 'python manage.py db upgrade', user=remote_user)
    for proc in remote_proc:
        sudo('systemctl restart %s' % proc)
