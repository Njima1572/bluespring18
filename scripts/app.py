from jrmap import JRMap
from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

jrm = JRMap()

@app.route('/')
def root():
    return "Root"

@app.route('/<latitude>/<longitude>/<n>')
def get_nearest_n_stations(latitude, longitude, n):
    station_list = jrm.get_nearest_station(float(longitude), float(latitude), int(n))
    print(json.dumps(station_list, ensure_ascii=False))
    return json.dumps(station_list, ensure_ascii=False)

@app.route('/<station_g_cd>')
def do_station_gacha(station_g_cd):
    station_name = jrm.data_manager.get_station_name_from_g_cd(int(station_g_cd))
    print(station_name)
    gacha_result = jrm.do_change_of_trains_gacha_g_cd(station_g_cd)

    strfy = f"At station: {station_list[0]} get on {gacha_result}"
    return strfy 


if __name__ == "__main__":
    app.run(debug=True)


