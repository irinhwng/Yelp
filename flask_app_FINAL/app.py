from flask import Flask, render_template, request, g, session, redirect, url_for
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
import requests
import pickle
from sklearn.ensemble import GradientBoostingRegressor

# create flask app
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# secret key to perform certain actions
app.secret_key = 'sdfgsdgfdgfgfdgd'

# create index
@app.route('/')
def index():

    return render_template("index.html")

# create dataframe page
@app.route('/dataframe/')
def dataframe():
    # read in dataframe
    df2 = pd.read_csv('MARIOdemoGRAPHS.csv').drop(columns='Unnamed: 0')

    return render_template("dataframe.html",data=df2.to_html())

# create team page
@app.route('/team/')
def team():

    return render_template("team.html")

# create map page
@app.route('/map/')
def map():
    # google static map scrape
    #key is confidential
    api_key = ""
    url = "https://maps.googleapis.com/maps/api/staticmap?"

    center = session['text'].strip()
    zoom = 15

    r = requests.get(url + "center=" +
        center + "&zoom=" + str(zoom) +
        "&size=400x400" + "&key=" + api_key)

    f = open("./static/images/map.png", "wb")
    f.write(r.content)
    f.close()

    return render_template("map.html",map_image=r.content)

# prediction function
def affluency_predictor(to_predict):
    # format the variable
    session_int = int(to_predict.strip())
    df = pd.read_csv("MARIO_MODEL_PCA.csv").drop(columns="Unnamed: 0")
    # create array from dataframe row
    predict_array = np.array(df[df['zip_code'] == session_int].drop(columns ='zip_code'))
    print(predict_array)
    # load trained model
    loaded_model = pickle.load(open("model_gb_mother.pkl", "rb"))
    # predict
    result = loaded_model.predict(predict_array)
    print(result)
    print('------------')
    return result[0]

@app.route('/process', methods=["POST"])
def process():
    if request.method == 'POST':

        results = affluency_predictor(request.form['rawtext'])

        # session variable
        session['text'] = request.form['rawtext']

        print(results)

        return render_template("index.html",results=np.round(results,2))

# create page to diplay visualization
@app.route('/histogram/')
def histogram():
    # test data
    # df2 = pd.read_csv('MARIOdemoGRAPHS.csv').drop(columns='Unnamed: 0')
    # train data
    df2 = pd.read_csv('MOTHEROFMOTHERS.csv').drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'])

    # use plotly to create visualization
    fig = make_subplots(rows=2, cols=2,
        subplot_titles=("Price 1", "Price 2", "Price 3", "Price 4"))

    fig.add_trace(go.Histogram(x=df2['Price_1']),
    row=1, col=1)

    fig.add_trace(go.Histogram(x=df2['Price_2']),
    row=1, col=2)

    fig.add_trace(go.Histogram(x=df2['Price_3']),
    row=2, col=1)

    fig.add_trace(go.Histogram(x=df2['Price_4']),
    row=2, col=2)

    fig.update_layout(height=700, width=900,
        title_text="Distribution of Train Data Price's ($$$$)", # title of plot

    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    histogram=graphJSON

    return render_template("histogram.html", plot=histogram)

@app.route('/bargraph/')
def create_plot():
    df2 = pd.read_csv('MARIOdemoGRAPHS.csv').drop(columns='Unnamed: 0')

    index = df2['zip_code'].values.tolist().index(int(session['text'].strip())) #returns 0

    listofprices = []
    for i in range(0, 1):
        p1 = df2['Price_1'][index]
        listofprices.append(p1)

        p2 = df2['Price_2'][index]
        listofprices.append(p2)

        p3 = df2['Price_3'][index]
        listofprices.append(p3)

        p4 = df2['Price_4'][index]
        listofprices.append(p4)

        objects = ['P1', 'P2', 'P3', 'P4']

        y = listofprices

    fig = go.Figure(data = [
        go.Bar(
            x=objects, y=listofprices
        )
    ])

    fig.update_layout(
    title_text='Zip Code Inputted Number of Businesses By Price Level', # title of plot
    xaxis_title_text='Price Level', # xaxis label
    yaxis_title_text='# of Businesses', # yaxis label
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    bargraph=graphJSON

    count = df2[df2['zip_code'] == int(session['text'].strip())]['count']

    return render_template("bargraph.html", plot=bargraph, count=int(count))

if __name__ == "__main__":
    app.run(debug=True)
