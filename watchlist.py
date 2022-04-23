import read_write_db
from collections import Counter


def handle_source_doughnut(company):
    print("inside handle_watch_list")
    all_data = read_write_db.get_column(TableName="processed_" + company, column="source")
    sources = []
    for src in all_data:
        sources.append(src["source"])

    sources_stats = dict(Counter(sources))
    sources= []
    stats = []
    print(sources_stats)
    for source_stat in sources_stats.items():
        print(source_stat)
        sources.append(source_stat[0])
        stats.append(source_stat[1])
    response = {"labels" : sources,  "dataset": stats }

    print(response)
    return response

def handle_bugs_source_doughnut(company):
    print("inside handle_watch_list")
    all_data = read_write_db.get_all_data(TableName="processed_" + company)
    sources = []
    for review in all_data:
        if review["highlightText"] == "":
            pass
        else:
            sources.append(review["source"])
    sources_stats = dict(Counter(sources))
    sources = []
    stats = []
    print(sources_stats)
    for source_stat in sources_stats.items():
        print(source_stat)
        sources.append(source_stat[0])
        stats.append(source_stat[1])
    response = {"labels": sources, "dataset": stats}

    print(response)
    return response




def handle_issues_line(company):
    response = read_write_db.get_all_data("processed_" + company )
    pdata = []
    graph_options = []
    month_based = {}

    for review in response:
        month = review["created_at"][:7]
        label = review["labels"][0]
        month_based.setdefault(month, []).append(label)

    print("month_based")
    graph_labels = sorted(list(month_based.keys()))
    final_topic_based_dates_count = {}
    for month, labels in month_based.items():
        # months = sorted(months)
        k = Counter(labels)
        # print(k)
        month_based = []
        k = dict(k)
        k["month"] = month
        pdata.append(k)
        graph_options.extend(set(labels))

        # for date, count in k.items():
        #     topic_dates_count = {}
        #     # print(date, count)
        #     topic_dates_count["month"] = date
        #     topic_dates_count["count"] = count
        #     # print("topic_dates_count :" , topic_dates_count)
        #     try:
        #         final_topic_based_dates_count[topic].append(topic_dates_count)
        #     except KeyError:
        #         final_topic_based_dates_count[topic] = [topic_dates_count]
        # break
    # graph_options = []
    # for k in final_topic_based_dates_count:
    #     graph_options.append({"name": k})
    # logger.info("graph_options")
    # logger.info(graph_options)
    graph_options = list(set(graph_options))
    # print("pdata")
    # print(pdata)
    # print(graph_options)
    #
    # response = {"pdata": pdata, "mixed_graph_options": graph_options}

    pdata = sorted(pdata, key=lambda k: k.get('month', 0), reverse=False)

    datasets = []
    for graph_option in graph_options:
        data = []
        for data_point in pdata:
            if graph_option in data_point:
                data.append(data_point[graph_option])
            else:
                data.append(0)
        datasets.append({"label": graph_option, "data": data})
    response = {"labels" : graph_labels, "datasets" : datasets}

    # print(datasets)
    print(response)

    return response


def handle_bugs_trend(company):
    response = read_write_db.get_all_data("processed_" + company)
    pdata = []
    graph_options = []
    month_based = {}
    monthly_issues = []

    for review in response:
        if review["highlightText"] == "":
            pass
        else:
            month = review["created_at"][:7]
            label = review["labels"][0]
            month_based.setdefault(month, []).append(label)
            monthly_issues.append(month)

    # print("month_based")

    graph_labels = sorted(list(month_based.keys()))
    # print(graph_labels)
    values = (dict(Counter(monthly_issues)))
    datasets = []
    for label in graph_labels:
        datasets.append(values[label])
    # print(datasets)
    response = {"labels": graph_labels, "datasets": datasets}
    print(response)

    return response


def feedback_trend(company):
    response = read_write_db.get_all_data("processed_" + company )
    pdata = []
    graph_options = []
    month_based = {}
    monthly_issues = []

    for review in response:
        month = review["created_at"][:7]
        label = review["labels"][0]
        month_based.setdefault(month, []).append(label)
        monthly_issues.append(month)

    # print("month_based")

    graph_labels = sorted(list(month_based.keys()))
    # print(graph_labels)
    values = (dict(Counter(monthly_issues)))
    datasets = []
    for label in graph_labels:
        datasets.append(values[label])
    # print(datasets)
    response = {"labels" : graph_labels, "datasets" : datasets}
    print(response)

    return response


def handle_wathcList(company_name):
    response_source_doughtnut = handle_source_doughnut(company_name)
    response_issues_line = handle_issues_line(company_name)
    response_issues_line2 = handle_bugs_trend(company_name)


    response_feedback_trend = feedback_trend(company_name)
    response_bugs_source_doughnut = handle_bugs_source_doughnut(company_name)

    return {"source_doughnut": response_source_doughtnut , "bugs_by_source_doughnut" : response_bugs_source_doughnut,
            "issues_topic_wise" : response_issues_line, "issues_topic_wise2" : response_issues_line2,  "feedback_trend" : response_feedback_trend }


if __name__ == '__main__':
    # response = handle_wathcList("roundpier")
    # print(response)
    # feedback_trend("roundpier")
    handle_bugs_source_doughnut("thursday")
    # sort = sorted(response["pdata"], key=lambda k: k.get('month', 0), reverse=False)
    # labels = []
    # mixed_graph_options = response["mixed_graph_options"]
    #
    # datasets = []
    # for graph_option in mixed_graph_options:
    #     data = []
    #     for data_point in sort:
    #         if graph_option in data_point:
    #             data.append(data_point[graph_option])
    #         else:
    #             data.append(0)
    #     datasets.append({"label": graph_option, "data": data})
    #
    # print(datasets)