#!/usr/bin/env python

from flask.ext.script import Manager
from flask.ext.script.commands import Clean, ShowUrls
from flask.ext.migrate import MigrateCommand
from gunicorn.app.wsgiapp import WSGIApplication

from ailtdou.app import create_app
from ailtdou.main.models import inbox as _inbox


app = create_app()
manager = Manager(app)

manager.add_command(Clean())
manager.add_command(ShowUrls())
manager.add_command('db', MigrateCommand)


@manager.command
def inbox(host='127.0.0.1', port=4467):
    """Watches inbox and handles incoming requests."""
    _inbox.serve(int(port), host)


@manager.command
def http(host='127.0.0.1', port=5000, workers=None):
    """Runs the app within Gunicorn."""
    workers = workers or app.config.get('WORKERS') or 1

    if app.debug:
        app.run(host, int(port))
    else:
        gunicorn = WSGIApplication()
        gunicorn.load_wsgiapp = lambda: app
        gunicorn.cfg.set('bind', '%s:%s' % (host, port))
        gunicorn.cfg.set('workers', workers)
        gunicorn.cfg.set('pidfile', None)
        gunicorn.cfg.set('accesslog', '-')
        gunicorn.cfg.set('errorlog', '-')
        gunicorn.chdir()
        gunicorn.run()


if __name__ == '__main__':
    manager.run()
