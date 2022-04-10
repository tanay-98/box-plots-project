from crypt import methods
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
        query = request.form.get('query')
        
        
        
        cur = mysql.connection.cursor()
        cur.execute(query)
        
        df = pd.DataFrame(cur.fetchall())

        #TODO - Delete this
        print(query)
        print(len(df))

        fig = px.box(df, y="SCORE", x="GRADE")

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template("base.html", graphJSON=graphJSON)

    return render_template("base.html")