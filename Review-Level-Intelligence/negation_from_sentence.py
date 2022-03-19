import spacy

nlp = spacy.load("en_core_web_sm")

# from nltk import pos_tag
from nltk import RegexpParser

# s = "First off I can't find my home town in the app, This is useless I cannot save my pic. I live and grew up in a Small town in Ohio and I can find it therefore I cannot complete my profile"


def gieven_sentence_give_chunk(s):
    doc = nlp(s)
    tokens_tags = []
    for token in doc:

        tokens_tags.append((token.text, token.pos_))

        # if token.pos_ == "PART":
        #     print(token.text)

    patterns= """actionchunk:{<AUX><PART><VERB><PRON|NOUN>*}"""
    # patterns= """actionchunk:{<AUX><.*>*<VERB><.*>*<PRON|NOUN>+}"""

    chunker = RegexpParser(patterns)
    output = chunker.parse(tokens_tags)

    for subtree in output.subtrees():
        if subtree.label() == 'actionchunk' and len(subtree)>1:
            print(subtree)

if __name__ == '__main__':
    s = "would never accept the person’s street address"
    gieven_sentence_give_chunk(s)