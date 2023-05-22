from MyWebApp.app import create_app
from MyWebApp.db_manager import DatabaseManager
from getpass import getpass

app = create_app()


if __name__ == '__main__':
    app.run()
