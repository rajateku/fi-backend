from transformers import pipeline


candidate_labels = ["recommendation" , "none"]
classifier = pipeline("zero-shot-classification") # to utilize GPU

s = "I would suggest to add google pay"
res = classifier(s, candidate_labels, multi_class=True)
print("Response : ", res )