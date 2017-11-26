if __name__ == '__main__':
    from flask_script import Manager
    from flask_migrate import MigrateCommand

    from config import HOST, PORT, DEBUG
    from app import app

    manager = Manager(app)

    manager.add_command('db', MigrateCommand)

    @manager.command
    def runserver(host=HOST, port=PORT, debug=DEBUG):
        """"
        Start server
        """
        app.run(host=host, port=int(port), debug=debug)

    @manager.command
    def maintenance():
        from app.maintenance import maintenance
        maintenance()

    manager.run()
