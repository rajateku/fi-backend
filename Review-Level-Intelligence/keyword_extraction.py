import spacy
import pandas as pd
from collections import Counter
nlp = spacy.load('en_core_web_sm')
all_nouns_rp = []
def spacy_nouns(sent):

    doc = nlp(sent)
    noun_phrases = set(chunk.text.strip().lower() for chunk in doc.noun_chunks)

    print("noun_phrases")
    print(noun_phrases)

    nouns = set()
    for token in doc:
        if token.pos_ == "NOUN":
            nouns.add(token.text)
    print(nouns)

    # all_nouns = nouns.union(noun_phrases)
    all_nouns = noun_phrases
    print(all_nouns)
    return all_nouns


df = pd.read_csv("/Users/rajateku/Documents/ACADEMICS/PROJECT/rt257/code/Data4/wise_612261027.csv")["review"]

for review in df:
    print(review)
    all_nouns = spacy_nouns(review)
    all_nouns_rp.extend(list(all_nouns))

print(Counter(all_nouns_rp))
