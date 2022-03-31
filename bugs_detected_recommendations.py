import read_write_db

# Python program to generate WordCloud

# importing all necessary modules
# from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
from graphs import get_mixed_graph_data_from_response, get_graph_data_from_response
import nltk

# from transformers import pipeline
# candidate_labels = ["recommendation", "none"]
# classifier = pipeline("zero-shot-classification")  # to utilize GPU


# def handle_recommendation_zero_shot_ml(review):
#
#     sentences = nltk.sent_tokenize(review)
#
#
#     for s in sentences:
#         # s = "I would suggest to add google pay"
#         res = classifier(s, candidate_labels, multi_class=True)
#         print(res)
#         if res["labels"][0] == "recommendation":
#             if res["scores"][0] >0.9:
#                 return s, res["scores"][0]
#     else:
#         return "" , ""




def handle_suggestions(company):
    print("inside handle_suggestions")
    all_data = read_write_db.get_all_data(TableName="processed_" + company)
    bugs_data = []
    for review in all_data:
        if review["suggestionText"] == "":
            pass
        else:
            bugs_data.append(review)
            print(review["suggestionText"], review["rating"])
        # res, score = handle_recommendation_zero_shot_ml(review["text"])
        # if res == "":
        #     pass
        # else:
        #     review["zero_shot_reco"] = res
        #     review["zero_shot_score"] = score
        #     bugs_data.append(review)
    print("finished handle_suggestions")

    suggestions_data = sorted(bugs_data, key=lambda k: k.get('created_at', 0), reverse=False)

    response = {}
    response["suggestions"] = suggestions_data


    return response

def handle_bugs(company):
    print("inside handle_bugs")
    all_data = read_write_db.get_all_data(TableName="processed_" + company)
    bugs_data = []
    for review in all_data:
        if review["highlightText"] =="":
            pass
        else:
            bugs_data.append(review)
            print(review["highlightText"], review["rating"])


        # bugs_data.append(review)

    print("finished handle_bugs")
    bugs_data = sorted(bugs_data, key=lambda k: k.get('created_at', 0), reverse=False)

    response = get_mixed_graph_data_from_response(bugs_data)
    response["bugs"] = bugs_data

    topic_based_dates_count, graph_options = get_graph_data_from_response(bugs_data)
    response["graphData"] = topic_based_dates_count
    response["graphDataOptions"] = graph_options
    response["graphDisplayOption"] = graph_options[0]["name"]


    return response

def handle_bugs_watch_list(company):
    print("inside handle_bugs")
    all_data = read_write_db.get_all_data(TableName="processed_" + company)
    bugs_data = []
    for review in all_data:
        if review["highlightText"] =="":
            pass
        else:
            bugs_data.append(review)
            print(review["highlightText"], review["rating"])


        bugs_data.append(review)

    print("finished handle_bugs")
    bugs_data = sorted(bugs_data, key=lambda k: k.get('created_at', 0), reverse=False)

    response = get_mixed_graph_data_from_response(bugs_data)
    response["bugs"] = bugs_data

    topic_based_dates_count, graph_options = get_graph_data_from_response(bugs_data)
    response["graphData"] = topic_based_dates_count
    response["graphDataOptions"] = graph_options
    response["graphDisplayOption"] = graph_options[0]["name"]


    return response





if __name__ == '__main__':
    company = "lyft"
    # comment_words = handle_bugs(company=company)
    # # stopwords = set(STOPWORDS)
    #
    # wordcloud = WordCloud(width=1200, height=800,
    #                       background_color='white',
    #                       stopwords=stopwords,
    #                       min_font_size=10).generate(comment_words)
    #
    # # plot the WordCloud image
    # plt.figure(figsize=(12, 8), facecolor=None)
    # plt.imshow(wordcloud)
    # plt.axis("off")
    # plt.tight_layout(pad=0)
    # plt.savefig("wordcloud.png")

    # plt.show()
