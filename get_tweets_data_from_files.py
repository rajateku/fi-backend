import requests
import json
import credentials, get_hashtag_for_search
import pandas as pd
import csv
import os

CSV_FOLDER = "Data4/"


def get_data_from_csv_file(query):
    CSV_FILE = CSV_FOLDER + "{}.csv".format(query)
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        a = list(reader)

    response = {"data": a}
    return response


if __name__ == '__main__':
    query = "@Deliveroo"
    json_response = get_data_from_csv_file(query=query)
    get_hashtag_for_search.json_to_hashtags(query, json_response)
