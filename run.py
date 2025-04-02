from app import create_app

flask_app = create_app()

if __name__ == '__main__':
    print(flask_app.config)
    flask_app.run(debug=True)


    