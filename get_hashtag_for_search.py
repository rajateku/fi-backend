from collections import Counter



def json_to_hashtags(search_term, search_results_json):
    big_hashtags = []
    print(len(search_results_json["data"]))

    for a in search_results_json["data"]:

        tweet_text = a["text"].lower()
        if tweet_text.__contains__("#"):
            splits = tweet_text.split()
            for split in splits:
                if split.startswith("#"):
                    big_hashtags.append(split)



    return str(Counter(big_hashtags))

