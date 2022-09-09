
from flask import Flask

app = Flask(__name__)

from API.api import api_blueprint
from Website.website import website_blueprint

app.register_blueprint(api_blueprint)
app.register_blueprint(website_blueprint)

if __name__ == "__main__":
    app.run()