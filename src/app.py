"""
While lightweight and easy to use, Flask's built-in server 
is not suitable for production as it doesn't scale well

We use 'waitress' or 'gunicorn' WSGI for production
"""

from flask import Flask
import config
from flask_socketio import SocketIO
from flask_cors import CORS

from flask_ngrok import run_with_ngrok


def create_app():

    app = Flask(__name__)
    # run_with_ngrok(app)

    # Establish connection to MongoDB Cluster
    try:
        from pymongo import MongoClient
        # drop your mongoDB uri as MONGO_URI in an env file
        client = MongoClient(config.MONGO_URI)
        # Connecting to main database client["DATABASE_NAME"]
        config.db = client["megathon"]
        # config.db.users.create_index([("location", GEO2D)])

        # print(config.db)
        print(' >>> Established connection to DB')
    except Exception as ex:
        print('Can not connect to DB=>'+str(ex))

    # Import blueprints
    from routes import test
    from routes.users import Uauth
    from routes.users import reports
    # Register Blueprints
    app.register_blueprint(test.test)
    app.register_blueprint(Uauth.user)
    app.register_blueprint(reports.file)
    # Enable CORS
    CORS(app)

    return app


if __name__ == '__main__':
    # Run this script only in development
    # Use 'waitress' or 'gunicorn' WSGI for production instead

    print("goin")
    app = create_app().run(host="0.0.0.0")
