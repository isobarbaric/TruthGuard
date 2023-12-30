from flask import Flask

app = Flask(__name__)

# from website.website import website_blueprint
from website.website import website_blueprint

# app.register_blueprint(api_blueprint)
app.register_blueprint(website_blueprint)

if __name__ == "__main__":
    app.run()