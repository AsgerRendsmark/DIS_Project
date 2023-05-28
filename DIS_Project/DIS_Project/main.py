from MyWebApp.app import create_app
from MyWebApp.db_manager import DatabaseManager
from getpass import getpass

app = create_app()


if __name__ == '__main__':
    print("Enter your database password")
    app.run(debug=True)
