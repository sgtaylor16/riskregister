from app import create_app
from extensions import db

flask_app = create_app()

if __name__ == '__main__':
    with flask_app.app_context():
        print(db.engine.url)
    flask_app.run(debug=True)


    