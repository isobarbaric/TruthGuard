
from flask import render_template, request, Blueprint

website_blueprint = Blueprint(
    'website',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/home-static'
)

@website_blueprint.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        print(request.form.get('query'))
        # if query-link, then process accordingly => have to distinguish between the two text boxes
        return render_template("result.html", text_content = request.form.get('query'))
    else:
        return render_template("index.html")
