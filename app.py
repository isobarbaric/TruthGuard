
from flask import Flask

app = Flask(__name__, template_folder='Website/templates')

import API.api
import Website.website

if __name__ == "__main__":
    app.run(debug=True)