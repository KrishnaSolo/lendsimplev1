from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def init_db(app):
    if os.environ.get("ENVIRONMENT") == "PRODUCTION":
        # Google Cloud SQL database configuration
        db_user = os.environ.get("CLOUD_SQL_USERNAME")
        db_password = os.environ.get("CLOUD_SQL_PASSWORD")
        db_name = os.environ.get("CLOUD_SQL_DATABASE_NAME")
        db_socket_dir = os.environ.get("DB_SOCKET_DIR")
        cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

        db_uri = f"postgresql+psycopg2://{db_user}:{db_password}@/{db_name}?host={db_socket_dir}/{cloud_sql_connection_name}"
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    else:
        # Local development database configuration
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.session.close_all()
        db.engine.dispose()
        db.drop_all()
        db.create_all()
        from backend.data_local_loader import insert_example_data

        insert_example_data()
