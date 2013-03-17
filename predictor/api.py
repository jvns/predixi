from flask import Flask, request, jsonify
from datetime import timedelta
from random import randint
import pandas as pd
app = Flask(__name__)

def create_response(data):
    response = jsonify(data)
    response.status_code = 200
    return response

def get_history(station_ids, times):
    return get_predictions(station_ids, times)

def get_predictions(station_ids, times):
    response = {}
    for station_id in station_ids:
        predictions = []
        numBikes = 20
        numDocks = 0
        for time in times:
            prediction = {}
            prediction["time"] = time
            numBikes += randint(-3, 3)
            numDocks += randint(-3, 3)
            prediction["nbBikes"] = numBikes
            prediction["nbEmptyDocks"] = numDocks
            predictions.append(prediction)
        response[station_id] = {
            "id": station_id,
            "predictions": predictions
        }
    return response

@app.route('/stations')
def route_get_station_list():
    data = {
        "stations": [1,2,3]
    }
    return create_response(data)

@app.route('/stations/<stationid>')
def route_get_station_info(stationid):
    data = {
        "id": stationid,
        "name": "Magic station",
        "terminalName": 111,
    }
    return create_response(data)

@app.route('/stations/<stationid>/predictions')
def route_get_station_predictions(stationid):
    return route_get_station_history(stationid)

@app.route('/stations/<stationid>/history')
def route_get_station_history(stationid):
    start = pd.to_datetime(request.args.get('start') or '2012-05-01')
    end = pd.to_datetime(request.args.get('end')) or start + timedelta(days=1)
    times = pd.date_range(start=start, end=end, freq='30min').map(lambda x: x.value / 1000000)
    data = get_history([stationid], times)
    return create_response(data)

@app.route('/stations/predictions')
def all_stations_predictions():
    if 'time' in request:
        return request.time


if __name__ == '__main__':
    app.debug = True
    app.run()
