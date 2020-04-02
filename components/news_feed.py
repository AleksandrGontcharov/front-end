import requests
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import cache
from utils.settings import NCOV19_API, STATES_COORD
import json


@cache.memoize(timeout=900)
def news_feed(state="US") -> dbc.ListGroup:
    """Displays news feed on the right hand side of the display. Adjust the NewsAPI time
    time to Eastern Time (w/ DST).
    
    TODO: Add callbacks to fetch local state news, if none get entire US news
    
    :params state: display news feed for a particular state. If None, display news feed
        for the whole US

    :return list_group: A bootstramp ListGroup containing ListGroupItem returns news feeds.
    :rtype: dbc.ListGroup    
    """

    if state == "US":
        response = requests.get(NCOV19_API + "news")
    else:
        payload = {"state": state, "topic": "coronavirus"}
        payload = json.dumps(payload)
        response = requests.post(NCOV19_API + "news", data=payload)
        
    if response.status_code == 200:
        json_data = response.json()
        json_data = json_data["message"]
        # df = pd.read_json(json_data)
        df = pd.DataFrame.from_records(json_data)
        df = pd.DataFrame(df[["title", "url", "published"]])

        max_rows = 50
        list_group = dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    [
                        html.H6(
                            f"{df.iloc[i]['title'].split(' - ')[0]}.",
                            className="news-txt-headline",
                        ),
                        html.P(
                            f"{df.iloc[i]['title'].split(' - ')[1]}  {df.iloc[i]['published']}",
                            className="news-txt-by-dt",
                        ),
                    ],
                    className="news-item",
                    href=df.iloc[i]["url"],
                    target="_blank",
                )
                for i in range(min(len(df), max_rows))
            ],
            flush=True,
        )

    else:
        list_group = []

    return list_group
