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
        return self.company_df.loc[self.company_df["rr_cd"] == company_id]

    # use rr_cd code to get lines
    def get_lines(self, company_id):
        sub_comapnies_cd = self.get_sub_companies(company_id)["company_cd"]
        return self.line_df.loc[self.line_df["company_cd"].isin(sub_comapnies_cd)]
    
    # use rr_cd code to get stations
    def get_stations(self, company_id):
        lines = self.get_lines(company_id)
        return self.station_df.loc[self.station_df["line_cd"].isin(lines["line_cd"])]

dm = DataManager()

jr_company_id = 11

print(dm.get_stations(jr_company_id))
