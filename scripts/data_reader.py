import os
import numpy as np
import pandas as pd

PROJ_ROOT = os.getenv("PROJ_ROOT")

station_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "station20200619free.csv"))
join_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "join20200619.csv"))

# print(station_df["station_cd"])
# print(join_df)

def get_usable_line_cd():
    line_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "line20200619free.csv"))
    # Getting only JR lines from "line_name"
    return line_df.loc[line_df["line_name"].str[:2] == "JR"]

get_usable_line_cd()

