import pandas as pd
# Importing spacy for NLP
import spacy
import torch

# Check if CUDA is available
if torch.cuda.is_available():
    # Set the GPU device to use
    device = torch.device("cuda:0")  # Assuming you want to use the first GPU
    print("Using CUDA device:", torch.cuda.get_device_name(device))
else:
    print("CUDA is not available, using CPU")

# Load the English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Define file names for positive and negative data
positive_file_name = "positive.csv"
negative_file_name = "negative.csv"

# Read positive and negative data from CSV files
positive = pd.read_csv(positive_file_name)
negative = pd.read_csv(negative_file_name)

# Display the last few rows of the positive data
print(positive.tail())

# Function to extract nouns from text data
def find_nouns(text_data):
    nouns = []
    for text in text_data:
        doc = nlp(text)
        for sentence in doc.sents:
            for token in sentence:
                if token.pos_ == "NOUN":
                    nouns.append(token.lemma_)
    return nouns
    
# Function to find the top ten keywords
def find_top_ten_keys(nouns):
    keywords_count = {}
    for word in nouns:
        if word in keywords_count:
            keywords_count[word] += 1
        else:
            keywords_count[word] = 1
    keywords_count = sorted(keywords_count.items(), key=lambda x: x[1], reverse=True)
    top_ten = keywords_count[:10] 
    return top_ten

# Extract nouns from positive and negative data
positive_label = find_nouns(positive['text'])
negative_label = find_nouns(negative['text'])

# Find top ten keywords for positive and negative data
positive_label = find_top_ten_keys(positive_label)
negative_label = find_top_ten_keys(negative_label)

# Write positive keywords to a text file
dict_str = str(positive_label)
with open("./positive_labels.txt", "w") as file:
    file.write(dict_str)

# Write negative keywords to a text file
dict_str = str(negative_label)
with open("./negative_labels.txt", "w") as file:
    file.write(dict_str)

# Print top ten keywords for positive and negative data
print("Positive:\n")
print(positive_label)
print("Negative:\n")
print(negative_label)
