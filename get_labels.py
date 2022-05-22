import pandas as pd
import nltk
import read_write_db
#
import spacy
# from spacytextblob.spacytextblob import SpacyTextBlob

def get_sentiment(review):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')
    doc = nlp(review)
    doc._.blob.polarity  # Polarity: -0.125
    doc._.blob.subjectivity  # Subjectivity: 0.9
    doc._.blob.sentiment_assessments.assessments  # Assessments: [(['really', 'horrible'], -1.0, 1.0, None), (['worst', '!'], -1.0, 1.0, None), (['really', 'good'], 0.7, 0.6000000000000001, None), (['happy'], 0.8, 1.0, None)]
    doc._.blob.ngrams()  # [WordList(['I', 'had', 'a']), WordList(['had', 'a', 'really']), WordList(['a', 'really', 'horrible']), WordList(['really', 'horrible', 'day']), WordList(['horrible', 'day', 'It']), WordList(['day', 'It', 'was']), WordList(['It', 'was', 'the']), WordList(['was', 'the', 'worst']), WordList(['the', 'worst', 'day']), WordList(['worst', 'day', 'ever']), WordList(['day', 'ever', 'But']), WordList(['ever', 'But', 'every']), WordList(['But', 'every', 'now']), WordList(['every', 'now', 'and']), WordList(['now', 'and', 'then']), WordList(['and', 'then', 'I']), WordList(['then', 'I', 'have']), WordList(['I', 'have', 'a']), WordList(['have', 'a', 'really']), WordList(['a', 'really', 'good']), WordList(['really', 'good', 'day']), WordList(['good', 'day', 'that']), WordList(['day', 'that', 'makes']), WordList(['that', 'makes', 'me']), WordList(['makes', 'me', 'happy'])]


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
"Deactivation Issues"  : ["account deactivated" , "deactivated"],
"Payment issues"  : ["payment"],
"High exchange rate"  : ["rate", "exchange rate"],
"Extra fees issue"  : ["extra fees", "unknown fees", "fees"],
"Card issues"  : ["card"],
"Verification process issue"  : ["verification"],
"Transfer not allowed"  : ["allowed"],
"Money delayed issue"  : ["delayed"],
"Late transfer issue"  : ["late", "delayed"],
"App Issues"  : ["touch id", "app"],
"Customer service"  : ["customer support", "customer service"],
# "other"  : []
}


list_neagtions_bug = [
                        "bug", "not working" , "does not work", "not at all working", "Doesn't work", "does not",
                        "crash", "never get notifications",
                        "not able to",
                        "can't" , "can’t", "cant", "couldn't" , "couldn’t" , "could not",  "cannot" ,
                        "unable" , "Getting error",
                        "don't", "will not",
                        "slow"
]

list_suggestions = ["suggest", "please add" , "would like to see" , "would like to" ,  ]

bugs_1star = ["issues" , "disappears"]

def review_to_suggestion(review):
    # sentences = review.split(". ")
    sentences = nltk.sent_tokenize(review)

    for s in sentences:
        for word in list_suggestions:
            if s.lower().__contains__(word.lower()):
                highlight =  s
                return highlight
    highlight = ""
    return highlight


def review_to_highlight(review):
    # sentences = review.split(". ")
    sentences = nltk.sent_tokenize(review)

    for s in sentences:
        for word in list_neagtions_bug:
            if s.lower().__contains__(word.lower()):
                # print(s, word)
                highlight =  s
                return highlight
    highlight = ""
    # if len(sentences)>1:
    #     highlight =  sentences[1]
    # else:
    #     highlight = sentences[0]

    return highlight

# topics = read_write_db.get_all_data(TableName="topics")

def review_to_topic(review, topics):

    review = review.lower()
    # for topic,values in topics_kws_map.items():
    for topic in topics:
        print(topic)
        for kw in topic["words"].split(", "):
            if len(kw.split())>1:
                if review.__contains__(kw):
                    return topic["topic"]
            else:
                if kw in review.split():
                    return topic["topic"]
    return "Other Issues"


if __name__ == '__main__':
    print("get labels")