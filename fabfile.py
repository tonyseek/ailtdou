from fabric import task


remote_host = 'szulabs.org'
remote_repo = '/srv/ailtdou.szulabs.org'
remote_user = 'ailtdou'
remote_proc = ['ailtdou', 'ailtdou-smtp']
github_repo = 'https://github.com/tonyseek/ailtdou.git'
envvar_exec = 'withenv /opt/virtualenvs/ailtdou/bin/'  # http://git.io/withenv


def sudo(c, command):
    c.sudo('bash -c "cd %s && %s"' % (remote_repo, command), user=remote_user)


@task(hosts=[remote_host])
def deploy(c):
    sudo(c, 'git remote set-url origin %s' % github_repo)
    sudo(c, 'git pull --ff-only origin master')
    with c.cd(remote_repo):
        c.run(envvar_exec + 'pip install -r requirements.txt')
    sudo(c, envvar_exec + 'python manage.py clean')
    sudo(c, envvar_exec + 'python manage.py db upgrade')
    for proc in remote_proc:
        c.sudo('systemctl restart %s' % proc)
