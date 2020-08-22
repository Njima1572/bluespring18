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

    def get_jr_sub_companies(self):
        # 11 seems to be a JR rr_code
        return self.company_df.loc[self.company_df["rr_cd"] == 11]

    def get_jr_lines(self):
        jr_sub_comapnies_cd = self.get_jr_sub_companies()["company_cd"]
        return self.line_df.loc[self.line_df["company_cd"].isin(jr_sub_comapnies_cd)]

dm = DataManager()


print(dm.get_jr_lines())
