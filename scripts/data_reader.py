import os
import pandas as pd

PROJ_ROOT = os.getenv("PROJ_ROOT")

station_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "station20200619free.csv"))
line_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "line20200619free.csv"))
join_df = pd.read_csv(os.path.join(PROJ_ROOT, "resources/data", "join20200619.csv"))

print(station_df)
print(line_df)
print(join_df)
