
topics_kws_map = {
"Account Deactivated Issue"  : ["account deactivated" , "deactivated"],
"Payment not received"  : ["payment"],
"High exchange rate"  : [ "exchange rate", "rate"],
"Extra fees issue"  : ["extra fees", "unknown fees", "fees"],
"Card transaction failed"  : ["card"],
"Verification process issue"  : ["verification"],
"Transfer not allowed"  : ["allowed"],
"Money delayed issue"  : ["delayed"],
"Late transfer issue"  : ["late"],
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
                    print(kw)
                    return review, topic
            else:
                if kw in review.split():
                    print(kw)
                    return review, topic

review = "I’ve used this app for quite sometime but for some reason, they started recently to provide poor service, rates are not good, if you lock a rate and the rate became not in their favor, they try anyway to escape and cancel it, no real resolution for issues, money take long time to arrive, it was about to cost me a fortune by losing big sum due to mistake from one of the customer service, so I decided to look for another service provider."
review, topic = review_to_topic(review)
print( topic)