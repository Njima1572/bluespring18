import os
import numpy as np
import pandas as pd

PROJ_ROOT = os.getenv("PROJ_ROOT")

# Bullet train data is for paid people

class DataManager:
    def __init__(self, company_id=-1, exclude_bullet=True):
        self.company_id = company_id
        self.station_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "station20200619free.csv"))
        self.join_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "join20200619.csv"))
        self.company_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "company20200619.csv"))
        self.line_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "line20200619free.csv"))

        self.station_df = self.station_df.sort_values("station_cd")
        self.exclude_bullet = exclude_bullet

    # use rr_cd code
    def get_sub_companies(self):
        # 11 seems to be a JR rr_code
        if self.company_id < 0:
            return self.company_df
        return self.company_df.loc[self.company_df["rr_cd"] == self.company_id]

    # use rr_cd code to get lines
    def get_lines(self):
        sub_comapnies_cd = self.get_sub_companies()["company_cd"]
        lines_df = self.line_df.loc[self.line_df["company_cd"].isin(sub_comapnies_cd)]
        if self.exclude_bullet:
            lines_df = lines_df.loc[self.line_df["line_cd"] > 10000]
        return lines_df

    # use rr_cd code to get stations
    def get_stations(self):
        return self.station_df

    def get_joins(self):
        lines = self.get_lines()
        return self.join_df.loc[self.join_df["line_cd"].isin(lines["line_cd"])]

    def generate_line_cd_name_dict(self):
        lines_df = self.get_lines()
        return lines_df.set_index('line_cd')['line_name_h'].to_dict()

    def generate_station_to_station_df_line_group(self):
        station_df = self.get_stations()
        station_grouped = station_df.groupby("station_g_cd")

        # Trying to get stations with multiple change of lines
        size_station_df = station_grouped.size().reset_index().rename(columns={"station_g_cd": "station_g_cd", 0:"count"})
        size_station_df = size_station_df.loc[size_station_df["count"] > 1]

        # Trying to make a groupby of each stations with changes
        stations_with_changes_df = station_df.loc[station_df["station_g_cd"].isin(size_station_df["station_g_cd"])]
        stations_with_changes_groupby = stations_with_changes_df.groupby("station_g_cd")

        return stations_with_changes_groupby.groups
    
    def generate_station_g_cd_to_data_dict(self):
        station_df = self.get_stations()
        station_dict = {}

        # rows = station_df.iterrows()
        rows = station_df.itertuples()
        for row in rows:
            station_dict[row[2]] = row[3:]
        
        return station_dict

    def generate_station_cd_g_cd_dict(self):
        station_df = self.get_stations()
        station_cd_g_cd_dict = {}

        rows = station_df.itertuples()
        for row in rows:
            station_cd_g_cd_dict[row[1]] = row[2]

        return station_cd_g_cd_dict

    def get_station_name_from_g_cd(self, station_g_cd):
        g_cd_dict = self.generate_station_g_cd_to_data_dict()
        return g_cd_dict[station_g_cd][0]


    
    def set_company_id(self, company_id):
        self.company_id = company_id

    def set_exclude_bullet(self, exclude_bullet):
        self.exclude_bullet = exclude_bullet


if __name__ == "__main__":
    jr_company_id = 30
    dm = DataManager(jr_company_id)
    # print(dm.get_stations(jr_company_id))
    # print(dm.generate_line_cd_name_dict(jr_company_id))
    # print(dm.get_lines(jr_company_id))
    # print(dm.get_lines(jr_company_id, exclude_bullet=False))
    # print(dm.generate_station_to_station_df_line_group())
    # print(dm.generate_station_g_cd_to_data_dict())
    # print(dm.get_joins_by_line_cd()[11342])



