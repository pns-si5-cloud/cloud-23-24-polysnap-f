from flask import Flask
from controllers import routes

app = Flask(__name__)

app.register_blueprint(routes.routes)

if __name__ == "__main__":
    app.run(port=5000)
