from flask import Blueprint, render_template, request
from matplotlib.pyplot import figure
from . import mysql
import pandas as pd
import plotly.express as px
import json
import plotly

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query_s = request.form.get('query')
        query_o = "SELECT * FROM Moody2022_new;"

        cur = mysql.connection.cursor()
        
        cur.execute(query_o)
        df = pd.DataFrame(cur.fetchall())
        print(len(df))
        fig = px.box(df, y="SCORE", x="GRADE")

        graphJSON_o = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        cur.execute(query_s)
        df = pd.DataFrame(cur.fetchall())
        print(df.head())
        fig = px.box(df, y="SCORE", x="GRADE")

        graphJSON_s = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


        return render_template("base.html", graphJSON_o=graphJSON_o, graphJSON_s=graphJSON_s)

    return render_template("base.html")