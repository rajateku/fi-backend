import pandas as pd

def get_phrases():
    df = pd.read_csv("Company Reviews - review_phrases.csv")
    phrases = list(df["phrases"])
    words = list(df["words"])
    features = list(df["features"])
    critical = list(df["critical"])
    csv_phrases = {
        "phrases" : phrases,
        "words" : words,
        "features" :features,
        "critical" :critical
    }
    return csv_phrases

csv_phrases = get_phrases()

sectors = {
    "food" : ["food" , "taste", "restaurants", "restaurant"],
    "riding" : ["refund", "delay", "late" , "ride", "discount", "experience", "driver", "cancel" , "waited", "drivers"],
    "delivery" : ["late", "order"],
    "tech" : ["app", "web", "account", "payment", "expensive" , "charge"],
    "phrases": csv_phrases["phrases"],
    "words" : csv_phrases["words"],
    "features" : csv_phrases["features"],
    "critical" : csv_phrases["critical"],
    "competitors" : [],
}




#
# def give_kws_list(sector_list):
#     kws_list = []
#     for sector in sector_list:
#         kws_list.extend(sectors[sector])
#     return kws_list

#
# def given_sentence_to_lables(s, sector_list):
#     labels = []
#     kws = give_kws_list(sector_list)
#     for tok in s.split():
#         if tok in kws:
#             labels.append(tok)
#     for phrase in sectors["phrases"]:
#         if s.lower().__contains__(phrase):
#             labels.append(phrase)
#     return labels

topics_kws_map = {
"Remitly"  : ["remitly"],
"Account Deactivated Issue"  : ["account deactivated" , "deactivated"],
"Payment not received"  : ["payment"],
"High exchange rate"  : ["rate", "exchange rate"],
"Extra fees issue"  : ["extra fees", "unknown fees", "fees"],
"Card transaction failed"  : ["card"],
"Verification process issue"  : ["verification"],
"Transfer not allowed"  : ["allowed"],
# "Money delayed issue"  : ["delayed"],
"Late transfer issue"  : ["late", "delayed"],
"App Issues"  : ["touch id", "app"],
"Customer support issues"  : ["customer support", "customer service"],
"other"  : []
}


def review_to_topic(review):
    review = review.lower()
    for topic,values in topics_kws_map.items():
        for kw in values:
            if len(kw.split())>1:
                if review.__contains__(kw):
                    return topic
            else:
                if kw in review.split():
                    return topic
    return "Other Issues"


if __name__ == '__main__':
    sentences = [
        "I have been using this app for 2 years and the past maybe 4-5 months the prices have increased exceptionally. There's also been a great amount of times I can't find a driver or/and I have waited for 30 min each time, until someone accepts my journey. A lot of drivers accept and after a couple minute...",
        "I wanted to support local but on the second cancellation fee time trying the app I couldn't order a bolt because the app said no one was available and I must try again later. They then billed me for the trip (which as I said, never happened because no one was available) I went through a maze of trying to find out ho...",
        ]

    for s in sentences:
        labels = given_sentence_to_lables(s, ["riding" , "tech"])
        print(s, labels)

