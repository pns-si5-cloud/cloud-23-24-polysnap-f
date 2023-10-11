from flask import Flask
from controllers import main_routes

app = Flask(__name__)

app.register_blueprint(main_routes)

if __name__ == "__main__":
    app.run(port=5000)
