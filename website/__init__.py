from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "hfgdjsjjshgdj"
    app.config['MYSQL_USER'] = 'admin'
    app.config['MYSQL_PASSWORD'] = '123456789'
    app.config['MYSQL_HOST'] = 'box-plots-project.cglzzehf528q.us-east-2.rds.amazonaws.com'
    app.config['MYSQL_DB'] = 'MOODY'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app
