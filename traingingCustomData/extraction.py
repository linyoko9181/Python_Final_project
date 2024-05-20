import pandas as pd
#spacy NLP
import spacy
import torch

# Check if CUDA is available
if torch.cuda.is_available():
    # Set the GPU device to use
    device = torch.device("cuda:0")  # Assuming you want to use the first GPU
    print("Using CUDA device:", torch.cuda.get_device_name(device))
else:
    print("CUDA is not available, using CPU")

nlp = spacy.load("en_core_web_sm")

positive_file_name = "positive.csv"
negative_file_name = "negative.csv"
positive = pd.read_csv(positive_file_name)
negative = pd.read_csv(negative_file_name)
print(positive.tail())

#extract noun from the sentence
def find_nouns(text_data):
    nouns = []
    for text in text_data:
        doc = nlp(text)
        for sentence in doc.sents:
            for token in sentence:
                if token.pos_ == "NOUN":
                    nouns.append(token.lemma_)
    return nouns
    
#find the top ten key
def find_top_ten_keys(nouns):
    keywords_count = {}
    for word in nouns:
        if word in keywords_count:
            keywords_count[word] += 1
        else:
            keywords_count[word] = 1
    keywords_count = sorted(keywords_count.items(), key=lambda x: x[1], reverse = True)
    top_ten = keywords_count[:10] 
    return top_ten

positive_label = find_nouns(positive['text'])
negative_label = find_nouns(negative['text'])

positive_label = find_top_ten_keys(positive_label)
negative_label  =find_top_ten_keys(negative_label)

dict_str = str(positive_label)
with open("./positive_labels.txt", "w") as file:
    file.write(dict_str)
dict_str = str(negative_label)
with open("./negative_labels.txt", "w") as file:
    file.write(dict_str)

print("Positive:\n")
print(positive_label)
print("Negative:\n")
print(negative_label)
