from flask import Flask, make_response, g
from flask import request
import requests
import json
import StringIO
import pandas as pd
from matplotlib.pylab import savefig
app = Flask(__name__)

@app.route("/")
def homepage():
    return route_station_history(3)

@app.route('/stations/<stationid>/history')
def route_station_history(stationid):
    r = requests.get("http://localhost:5000/stations/{id}/history".format(id=stationid), params=request.args)
    image_base64 = base64_graph(r, stationid)
    image = '<img src="data:image/png;base64,%s" />' % image_base64
    return make_response(image)

@app.route('/stations/<stationid>/predictions')
def route_station_predictions(stationid):
    r = requests.get("http://localhost:5000/stations/{id}/predictions".format(id=stationid), params=request.args)
    image_base64 = base64_graph(r, stationid)
    image = '<img src="data:image/png;base64,%s" />' % image_base64
    return make_response(image)


def base64_graph(response, stationid):
    df = pd.DataFrame(json.loads(response.text)[str(stationid)]['predictions'])
    df.time = pd.to_datetime(df.time * 1000000)
    df.index = df.time
    df = df.drop('time', axis = 1)
    df[['nbBikes']].plot(figsize=(13, 4))
    output = StringIO.StringIO()
    savefig(output, format="png")
    contents = output.getvalue().encode("base64")
    output.close()
    return contents

if __name__ == '__main__':
    app.debug = True
    app.run('localhost', 5001)
    g.api_server = "http://localhost:5000"
