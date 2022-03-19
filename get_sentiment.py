# import spacy
# from spacytextblob.spacytextblob import SpacyTextBlob
# nlp = spacy.load('en_core_web_md')
# nlp.add_pipe('spacytextblob')
# from langdetect import detect


def give_sentiment(s):
    doc = nlp(s)
    polarity = doc._.blob.polarity
    if polarity <0:
        sentiment = "Negative"
    else:
        sentiment = "Positive"
    return sentiment, polarity


if __name__ == '__main__':
    sentiment = give_sentiment("This is bad")
    print(sentiment)