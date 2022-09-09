
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
    # print(request.method)
    print(request.form)
    article_link = request.form.get('article-link')
    article_body = request.form.get('article-text')
    print(article_body)
    print(article_link)

    # print(request.form[0])
    # if request.method == 'POST':
        # print(request.form)
        # a = request.form['article-link']
        # print(a)
        # if query-link, then process accordingly => have to distinguish between the two text boxes
        # return render_template("result.html", text_content = a)
    # else:
    return render_template("index.html")