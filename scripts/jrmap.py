import random
import math
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from data_manager import DataManager

JRCODE = 0

class JRMap:
    def __init__(self):
        self.data_manager = DataManager(JRCODE)
        self.graph = nx.Graph()
        self.construct_graph()

    def construct_graph(self):
        stations_df = self.data_manager.get_stations()
        station_cd_g_cd_dict = self.data_manager.generate_station_cd_g_cd_dict()
        joins = self.data_manager.get_joins()
        rows = stations_df.itertuples()

        # Adding nodes
        for row in rows:
            self.graph.add_node(row.station_g_cd)

        # Adding edges
        for line in joins.itertuples():
            src_cd = line.station_cd1
            dst_cd = line.station_cd2
            src_g_cd = station_cd_g_cd_dict[src_cd]
            dst_g_cd = station_cd_g_cd_dict[dst_cd]
            # print(line.line_cd)
            self.graph.add_edge(src_g_cd, dst_g_cd, line_cd=line.line_cd)
        # print(self.graph.edges.data())

    def visualize_nodes(self):
        station_g_cd_dict = self.data_manager.generate_station_g_cd_to_data_dict()
        lon_pts = []
        lat_pts = []
        for node in self.graph.nodes:

            data = station_g_cd_dict[node]
            lon = float(data[7])
            lat = float(data[8])
            lon_pts.append(lon)
            lat_pts.append(lat)

        plt.scatter(lon_pts, lat_pts, s=0.4)
        plt.show()

    def visualize_map(self):
        print("visualize_map")
        station_g_cd_dict = self.data_manager.generate_station_g_cd_to_data_dict()
        line_station_dict = {}

        for edge in self.graph.edges.data():
            src_idx = edge[0]
            dst_idx = edge[1]
            src_data = station_g_cd_dict[src_idx]
            dst_data = station_g_cd_dict[dst_idx]

            line_cd = edge[2]["line_cd"]

            if not line_cd in line_station_dict:
                line_station_dict[line_cd] = {"src": [], "dst": []}

            line_station_dict[line_cd]["src"].append(src_idx)
            line_station_dict[line_cd]["dst"].append(dst_idx)

        for line_cd in line_station_dict:
            # stations = np.unique(line_station_dict[line_cd])
            srcs = line_station_dict[line_cd]["src"]
            dsts = line_station_dict[line_cd]["dst"]
            color = np.random.rand(3, )

            # print(line_cd, stations)
            line_lon = []
            line_lat = []

            for src, dst in zip(srcs, dsts):
                src_data = station_g_cd_dict[src]
                dst_data = station_g_cd_dict[dst]
                # line_lon.append(float(src_data.lon))
                # line_lat.append(float(src_data.lat))
                src_lon = src_data[7]
                src_lat = src_data[8]
                dst_lon = dst_data[7]
                dst_lat = dst_data[8]
                plt.plot([src_lon, dst_lon], [src_lat, dst_lat], c=color)

        plt.show()

    def get_nearest_station(self, lon, lat, nums=1):
        stations_df = self.data_manager.get_stations()
        station_dist_dict = {}
        for station_data in stations_df.itertuples():
            station_lon = station_data.lon
            station_lat = station_data.lat

            squared_diff_lon = math.pow(lon - station_lon, 2)
            squared_diff_lat = math.pow(lat - station_lat, 2)

            station_dist_dict[station_data.station_g_cd] = squared_diff_lon + squared_diff_lat

        dist_sorted = sorted(station_dist_dict.items(), key=lambda x:x[1])
        
        station_names = []
        station_g_cds = []

        for i in range(nums):
            station_g_cd = dist_sorted[i][0]
            station_g_cds.append(station_g_cd)
            station_names.append(self.data_manager.get_station_name_from_g_cd(station_g_cd))

        return station_names, station_g_cds

    def do_change_of_trains_gacha(self, station_name):
        station_data = self.data_manager.get_station_data_from_name(station_name)
        print(station_data)
        randomint = random.randint(0, station_data["line_cd"].size - 1) 
        print(randomint)
        
        line_cd = station_data.values[randomint][5]

        return self.data_manager.get_line_cd_to_line_name(line_cd)

    def do_change_of_trains_gacha_g_cd(self, station_g_cd):
        station_data = self.data_manager.get_station_data_from_g_cd(station_g_cd)
        randomint = random.randint(0, station_data["line_cd"].size - 1) 
        print(randomint)
        
        line_cd = station_data.values[randomint][5]

        return self.data_manager.get_line_cd_to_line_name(line_cd)


def main():
    jrm = JRMap()
    # jrm.visualize_map()

    lat = 35.534129
    lon = 137.791698

    # print(jrm.get_nearest_station(lon, lat, 5))
    station_name = "川崎"
    print(f"{station_name}: {jrm.do_change_of_trains_gacha(station_name)}")


if __name__ == "__main__":
    main()
