import numpy as np
from pymongo import MongoClient
from datetime import datetime
from data_manager import DataManager


class StationsDB(object):

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['bluespring18']
        self.station_collecition= self.db['stations']
        self.line_collection= self.db['lines']
        # self.routes = self.db['routes']

        data_manager = DataManager()
        self.station_df = data_manager.station_df


    def add_one(self, station_g_cd):
        station_data = self.station_df.loc[self.station_df["station_g_cd"].isin([station_g_cd])]
        print(station_data)

        # Not sure what to do with station_cd
        post  = {
                'station_cd': int(station_data["station_cd"].values[0]),
                'station_g_cd': int(station_g_cd),
                'station_name': station_data["station_name"].values[0],
                'line_cd': int(station_data["line_cd"].values[0]),
                'pref_cd': int(station_data["pref_cd"].values[0]), 
                'post': station_data["post"].values[0],
                'address': station_data["address"].values[0],
                'coordinates': [float(station_data["lon"].values[0]), float(station_data["lat"].values[0])]
        }

        return self.db.test.insert_one(post)

    def add_station(self, station_g_cd):

        """
        post  = {
                'station_cd': ,
                'station_g_cd': station_g_cd,
                'station_name': ,
                'line_cd': ,
                'pref_cd': , 
                'post': ,
                'address': ,
                'coordinates': datetime.now(), # [longtitude, latitude]
        }
        return self.db.test.insert_one(post)
        """


def main():
    obj = StationsDB()
    obj.add_one(1130101)


if __name__ == "__main__":
    main()

