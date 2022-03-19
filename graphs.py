from collections import Counter
from logging_python import logger

def get_graph_data_from_response(response):
    topic_based = {}

    for review in response:
        date =review["created_at"][:7]
        label = review["labels"][0]
        topic_based.setdefault(label, []).append(date)


    # print(topic_based)
    final_topic_based_dates_count = {}
    for topic, dates in topic_based.items():
        dates = sorted(dates)
        k = Counter(dates)
        # print(k)
        topic_based[topic] = []
        for date, count in k.items():
            topic_dates_count = {}
            # print(date, count)
            topic_dates_count["month"] = date
            topic_dates_count["count"] = count
            # print("topic_dates_count :" , topic_dates_count)
            try:
                final_topic_based_dates_count[topic].append(topic_dates_count)
            except KeyError:
                final_topic_based_dates_count[topic] = [topic_dates_count]
        # break
    graph_options = []
    for k in final_topic_based_dates_count:
        graph_options.append({"name": k})
    logger.info("graph_options")
    logger.info(graph_options)
    return  final_topic_based_dates_count, graph_options

if __name__ == '__main__':
    # k = Counter(['2019-04', '2019-10', '2021-03'])
    # print(k)
    # topic_dates_count = {}
    # for date, count  in k.items():
    #     topic_dates_count["month"] = date
    #     topic_dates_count["count"] = count
    # print(topic_dates_count)

    gd = {'App Issues': [{'month': '2019-12', 'count': 1}, {'month': '2020-07', 'count': 1},
                    {'month': '2019-05', 'count': 1}, {'month': '2021-01', 'count': 1},
                    {'month': '2021-06', 'count': 2}, {'month': '2018-07', 'count': 2},
                    {'month': '2020-03', 'count': 1}, {'month': '2020-06', 'count': 2},
                    {'month': '2020-10', 'count': 1}, {'month': '2018-09', 'count': 1}],
     'Other Issues': [{'month': '2020-06', 'count': 1}, {'month': '2018-07', 'count': 2},
                      {'month': '2022-01', 'count': 1}, {'month': '2020-02', 'count': 1}]}
    graph_options = []
    for k in gd:
        graph_options.append({"name" : k})
        print(graph_options)
        print({"name" : k})
