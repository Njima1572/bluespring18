import os
import numpy as np
import pandas as pd

PROJ_ROOT = os.getenv("PROJ_ROOT")


class DataManager:
    def __init__(self):
        self.station_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "station20200619free.csv"))
        self.join_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "join20200619.csv"))
        self.company_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "company20200619.csv"))
        self.line_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "line20200619free.csv"))

    # use rr_cd code
    def get_sub_companies(self, company_id):
        # 11 seems to be a JR rr_code
        if compnay_id < 0:
            return self.compnay_df
        return self.company_df.loc[self.company_df["rr_cd"] == company_id]

    # use rr_cd code to get lines
    def get_lines(self, company_id, exclude_bullet=True):
        sub_comapnies_cd = self.get_sub_companies(company_id)["company_cd"]
        lines_df = self.line_df.loc[self.line_df["company_cd"].isin(sub_comapnies_cd)]
        if exclude_bullet:
            lines_df = lines_df.loc[self.line_df["line_cd"] > 10000]
        return lines_df
    # use rr_cd code to get stations
    def get_stations(self, company_id, exclude_bullet=True):
        lines = self.get_lines(company_id, exclude_bullet)
        return self.station_df.loc[self.station_df["line_cd"].isin(lines["line_cd"])]

    def generate_line_cd_name_dict(self, company_id):
        lines_df = self.get_lines(company_id)
        return lines_df.set_index('line_cd')['line_name_h'].to_dict()

    def genrate_station_to_station_df_line_group(self, company_id):
        station_df = self.get_stations(company_id)
        station_grouped = station_df.groupby("station_g_cd")

        # Trying to get stations with multiple change of lines
        size_station_df = station_grouped.size().reset_index().rename(columns={"station_g_cd": "station_g_cd", 0:"count"})
        size_station_df = size_station_df.loc[size_station_df["count"] > 1]

        # Trying to make a groupby of each stations with changes
        stations_with_changes_df = station_df.loc[station_df["station_g_cd"].isin(size_station_df["station_g_cd"])]
        stations_with_changes_groupby = stations_with_changes_df.groupby("station_g_cd")

        return stations_with_changes_groupby.groups


if __name__ == "__main__":
    dm = DataManager()
    jr_company_id = 11
    # print(dm.get_stations(jr_company_id))
    # print(dm.generate_line_cd_name_dict(jr_company_id))
    # print(dm.get_lines(jr_company_id))
    # print(dm.get_lines(jr_company_id, exclude_bullet=False))
    dm.generate_station_to_line_map(jr_company_id)



