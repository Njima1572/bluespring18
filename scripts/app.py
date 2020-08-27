from jrmap import JRMap
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

jrm = JRMap()

@app.route('/')
def root():
    return "Root"

@app.route('/<latitude>/<longitude>')
def location(latitude, longitude):
    station_list = jrm.get_nearest_station(float(longitude), float(latitude), 5)
    gacha_result = jrm.do_change_of_trains_gacha(station_list[0])

    strfy = f"At station: {station_list[0]} get on {gacha_result}"
    return strfy 


if __name__ == "__main__":
    app.run(debug=True)


