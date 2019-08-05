from flask import Flask, render_template, request, g, session, redirect, url_for
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import json
import requests

# create flask app
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# secret key to perform certain actions... this is random
app.secret_key = 'sdfgsdgfdgfgfdgd'

# def create_plot():
#     df = pd.read_csv("diabetes.csv")
#
#     data = [
#         go.Histogram(
#             x=df['Glucose']
#         )
#     ]
#
#     graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON

# create index
@app.route('/')
def index():

    return render_template("index.html")

# create dataframe page
@app.route('/dataframe/')
def dataframe():
    # read in dataframe
    df = pd.read_csv('MOTHEROFMOTHERS.csv').drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1']).head(20)

    return render_template("dataframe.html",data=df.to_html())

# create team page
@app.route('/team/')
def team():

    return render_template("team.html")

# create map page
@app.route('/map/')
def map():
    # google static map scrape
    #api key is confidential
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

# # prediction function
# def affluency_predictor(to_predict):
#     # format the variable
#     session_int = int(session['text'].strip())
#     # create array from dataframe row
#     to_predict = np.array(df[df['zip_code'] == session_int])
#     # load trained model
#     loaded_model = pickle.load(open("model.pkl", "rb"))
#     # predict
#     result = loaded_model.predict(to_predict)
#
#     return result

@app.route('/process', methods=["POST"])
def process():
    if request.method == 'POST':
        session['text'] = request.form['rawtext']
        df = pd.read_csv('MOTHEROFMOTHERS.csv').drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'])
        session_int = int(session['text'].strip())
        results = df[df['zip_code'] == session_int]['count']
                # = affluency_predictor(to_predict)
        return render_template("index.html",results=int(results))

# create page to diplay visualization
@app.route('/histogram/')
def histogram():
    df = pd.read_csv('MOTHEROFMOTHERS.csv').drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'])
    # use plotly to create visualization
    data = [
        go.Histogram(
            x=df['count']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    histogram=graphJSON

    return render_template("histogram.html", plot=histogram)

if __name__ == "__main__":
    app.run(debug=True)
