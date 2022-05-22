import nltk

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
}

bug_phrases = [
        "bug", "not working" , "does not work", "not at all working", "Doesn't work", "does not",
        "crash", "never get notifications",
        "not able to",
        "can't" , "can’t", "cant", "couldn't" , "couldn’t" , "could not",  "cannot" ,
        "unable" , "Getting error",
        "don't", "will not",
        "slow"
]

recommendation_phrases = ["suggest", "please add" , "would like to see" , "would like to", "I'd recommend" , "I would recommend", "wish it" , "I kinda wish" , "it would be most helpful", "would be a huge benefit" , "would be great"]

def review_to_suggestion(review):
    sentences = nltk.sent_tokenize(review)

    for s in sentences:
        print("sentence :", s)
        for word in recommendation_phrases:
            if s.lower().__contains__(word.lower()):
                highlight =  s
                print("suggestion : ", highlight)

                return highlight
    highlight = ""
    return highlight


def review_to_highlight(review):
    sentences = nltk.sent_tokenize(review)

    for s in sentences:
        for word in bug_phrases:
            if s.lower().__contains__(word.lower()):
                highlight =  s
                return highlight
    highlight = ""
    return highlight


def review_to_topic(review, topics):
    review = review.lower()
    topics_detected = []
    for topic in topics:
        for kw in topic["words"].lower().split(","):
            if len(kw.split())>1:
                if review.__contains__(kw):
                    topics_detected.append(topic["topic"])
            else:
                if kw in review.split():
                    topics_detected.append(topic["topic"])

    topics_detected = list(set(topics_detected))
    if len(topics_detected)<1:
        topics_detected = ["Other"]
    return topics_detected


if __name__ == '__main__':
    print("get labels")
    review_to_suggestion("Maye because it’s on the mobile app and most of the people use the desktop version, so I would recommend adding this feature to the website")