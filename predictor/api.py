from flask import Flask, request, jsonify
from random import randint
app = Flask(__name__)

def create_response(data):
    response = jsonify(data)
    response.status_code = 200
    return response

def get_predictions(station_ids, times):
    response = {}
    for station_id in station_ids:
        predictions = {}
        for time in times:
            predictions["time"] = time
            predictions["nbBikes"] = randint(1, 20)
            predictions["nbEmptyDocks"] = randint(1, 20)
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
    data = get_predictions([stationid], [10000])
    return create_response(data)

@app.route('/stations/<stationid>/history')
def route_get_station_history(stationid):
    data = get_predictions([stationid], [10000])
    return create_response(data)

@app.route('/stations/predictions')
def all_stations_predictions():
    if 'time' in request:
        return request.time


if __name__ == '__main__':
    app.debug = True
    app.run()

