from flask import Blueprint, flash, render_template, request
from matplotlib.pyplot import legend, title
from . import mysql
import pandas as pd
import plotly.graph_objects as go
import json
import plotly

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        grade_col = {'A':'#1f77b4', 'B':'#ff7f0e', 'C':'#2ca02c', 'D':'#d62728', 'E':'#9467bd', 'F':'#8c564b'}
        
        query_o = "SELECT * FROM Moody2022_new;"

        cur = mysql.connection.cursor()
        
        cur.execute(query_o)
        df = pd.DataFrame(cur.fetchall())
        print(query_o, "executed successfully. Shape of results - ", df.shape)
        fig = go.Figure()
        for grade in grade_col:
            fig.add_trace(go.Box(y=df[df.GRADE.eq(grade)]['SCORE'], name=grade, 
            marker_color=grade_col[grade]))
        fig.update_layout(
            title=query_o,
            legend_title="GRADES")

        graphJSON_o = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        if request.form['submit_btn'] == 'sq1':
            query_s = "SELECT * FROM Moody2022_new WHERE DOZES_OFF='always';"
        elif request.form['submit_btn'] == 'sq2':
            query_s = "SELECT * FROM Moody2022_new WHERE PARTICIPATION < 0.2;"
        elif request.form['submit_btn'] == 'sq3':
            query_s = "SELECT * FROM Moody2022_new WHERE PARTICIPATION > 0.5 and TEXTING_IN_CLASS='never';"
        else:
            query_s = request.form.get('query')
        
        try:
            
            cur.execute(query_s)
            df = pd.DataFrame(cur.fetchall())
            print(query_s, "executed successfully. Shape of results", df.shape)

            fig = go.Figure()
            for grade in grade_col:
                fig.add_trace(go.Box(y=df[df.GRADE.eq(grade)]['SCORE'], name=grade, 
                marker_color=grade_col[grade]))
            fig.update_layout(
                title=query_s,
                legend_title="GRADES")        

            graphJSON_s = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


            return render_template("base.html", graphJSON_o=graphJSON_o, graphJSON_s=graphJSON_s)
        except:
            flash("Incorrect query", category='error')

    return render_template("base.html")