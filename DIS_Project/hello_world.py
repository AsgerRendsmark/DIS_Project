from MyWebApp.app import create_app
from MyWebApp.db_manager import DatabaseManager



if __name__ == '__main__':
    # Start a separate thread to run the app
    app = create_app()
    print("Running app")
    app.run(debug=True)
    # Thread(target=run_app).start()