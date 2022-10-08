from flask import render_template, current_app as app


@app.route('/', methods=['GET'])
def index_get():
    return render_template("index.html")


@app.route('/articles', methods=['GET'])
def articles_get():
    return render_template("articles.html")
