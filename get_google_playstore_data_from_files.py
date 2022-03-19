import requests
import json
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
    playstore_handle = "com.roundpier.roundpier"

    query = playstore_handle
    json_response = get_data_from_csv_file(query=query)
