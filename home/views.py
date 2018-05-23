from flask import render_template, redirect, url_for

baseTemplate = 'index.html'


from flask import Blueprint

home_blueprint = Blueprint('home', __name__, template_folder='templates')


@home_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@home_blueprint.route('/navitem1', methods=['GET'])
def navitem1():
    return redirect(url_for('home.index'))


@home_blueprint.route('/navitem2', methods=['GET'])
def navitem2():
    return redirect(url_for('home.index'))


