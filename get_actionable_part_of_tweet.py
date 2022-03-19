
s = "Can't log into the app - no one answers the phone - terrible"

import spacy
# from negspacy.negation import Negex

nlp = spacy.load("en_core_web_sm")
doc = nlp(u"Can't log into the app")


negation_tokens = [tok for tok in doc if tok.dep_ == 'neg']
print(doc)

negation_head_tokens = [token.head for token in negation_tokens]

for token in negation_head_tokens:
    print(token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])

#
# def get_action_part(sentence):
#
#
#     sentence_action =  sentence
#     print(sentence_action)
#
#     return sentence_action
#
#
# get_action_part(s)
