import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from data_manager import DataManager

JRCODE = 11

class JRMap:
    def __init__(self):
        self.data_manager = DataManager(JRCODE)
        self.graph = nx.Graph()
        self.construct_graph()

    def construct_graph(self):
        stations_df = self.data_manager.get_stations()
        rows = stations_df.itertuples()
        for row in rows:
            self.graph.add_node(row[2])
        first = True
        for node, node_g_cd in zip(stations_df["station_cd"], stations_df["station_g_cd"]):
            if first:
                first = False
                prev_node = node
                prev_node_g_cd = node_g_cd
                continue

            if prev_node + 1 == node:
                self.graph.add_edge(prev_node_g_cd, node_g_cd)
            prev_node = node

    def visualize_map(self):
        station_g_cd_dict = self.data_manager.generate_station_g_cd_to_data_dict()
        # TODO: Optimize this loop
        # TODO: Add edges
        for node in self.graph.nodes:

            data = station_g_cd_dict[node]
            lon = float(data[7])
            lat = float(data[8])
            plt.scatter(lon, lat, s=0.4)

        plt.show()

    def filter_by_prefecture(self, pref_cd):
        station_g_cd_dict = self.data_manager.generate_station_g_cd_to_data_dict()
        pref_nodes = []
        for node in self.graph.nodes:
            data = station_g_cd_dict[node]
            data_pref_cd = int(data[4])
            if pref_cd == data_pref_cd:
                pref_nodes.append(data)

        return pref_nodes




def main():
    jrm = JRMap()
    jrm.visualize_map()


if __name__ == "__main__":

    main()
