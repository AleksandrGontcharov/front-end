import requests
import pandas as pd

from ncov19_dash import config
from ncov19_dash.config import DataReadingError


try:
    URL = config.NCOV19_API + config.COUNTY
    response = requests.get(URL).json()
    data = response["message"]

    data = pd.DataFrame.from_records(data)
    data["state_name"] = data["state_name"].str.title()
    # confirmed = data.groupby(["state_name"])["confirmed"].sum()
    # confirmed = confirmed.sort_values(ascending=False).to_dict()

    # death = data.groupby(["state_name"])["death"].sum()
    # death = death.sort_values(ascending=False).to_dict()
    last_updated = data["last_update"][0]

except DataReadingError as ex:
    print(f"[ERROR]: {ex}")


STATES = list(set(data["state_name"].to_list()))

del response, data
