if __name__ == '__main__':
    from flask.ext.script import Manager
    from flask.ext.migrate import MigrateCommand

    from config import HOST, PORT, DEBUG
    from app import app

    manager = Manager(app)

    manager.add_command('db', MigrateCommand)

    @manager.command
    def runserver(host=HOST, port=PORT, debug=DEBUG):
        "Start server"
        app.run(host=host, port=port, debug=debug)

    manager.run()
