
from flask import Flask, render_template, request, redirect, url_for
from newspaper import Article

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        print(request.form.get('query'))
        # if query-link, then process accordingly => have to distinguish between the two text boxes
        return render_template("result.html", text_content = request.form.get('query'))
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
