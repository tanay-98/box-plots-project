from unicodedata import category
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
    dataset = pd.read_csv('website/moody2022_new.csv').to_json(orient='records')

    if request.method == 'POST':
        
        query_o = "SELECT * FROM Moody2022_new;"

        cur = mysql.connection.cursor()
        
        cur.execute(query_o)
        df_o = pd.DataFrame(cur.fetchall())
        df_o['src'] = 0
        print(query_o, "executed successfully. Shape of results - ", df_o.shape)



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
            df_s = pd.DataFrame(cur.fetchall())
            df_s['src'] = 1
            print(query_s, "executed successfully. Shape of results", df_s.shape)
            df_s = pd.concat([df_o, df_s])

            fig = go.Figure()
            fig.add_trace(go.Box(
                y=df_s[df_s['src']==0]['SCORE'], 
                x=df_s[df_s['src']==0]['GRADE'],
                name="Zero", 
                marker_color="#1f77b4"
                ))
            
            print(df_s[df_s['src']==1]['SCORE'].shape)

            fig.add_trace(go.Box(
                y=df_s[df_s['src']==1]['SCORE'], 
                x=df_s[df_s['src']==1]['GRADE'],
                name="Sliced", 
                marker_color="#ff7f0e"
                ))
            
            fig.update_layout(
                title=query_s,
                legend_title="GRADES",
                boxmode='group'
                )

            fig.update_xaxes(
                categoryorder='array',
                categoryarray = ['A', 'B', 'C', 'D', 'F']
            )        

            graphJSON_s = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


            return render_template("base.html", graphJSON_s=graphJSON_s, dataset=dataset)
        except:
            flash("Incorrect query", category='error')

    return render_template("base.html", dataset=dataset)