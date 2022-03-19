import csv
from logging_python import logger

CSV_FOLDER = "Data4/"


def get_data_from_csv_file(query):
    CSV_FILE = CSV_FOLDER + "{}.csv".format(query)
    logger.info("opened csv file")
    logger.info(CSV_FILE)

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        a = list(reader)

    response = {"data": a}
    return response


if __name__ == '__main__':
    appstore_handle = "tiktok_835599320"
    query = appstore_handle
    json_response = get_data_from_csv_file(query=query)
