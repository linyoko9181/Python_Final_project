import spacy
import random
import pandas as pd

# Function to select a random sentence containing a specified word
def text_selector(sentiment, string):

    # Load spaCy's English model
    nlp = spacy.load("en_core_web_sm")

    # Function to find labels in text data
    def find_labels(text_data, string):
        sentence_index = []
        for i, text in enumerate(text_data):
            doc = nlp(text)
            for sentence in doc.sents:
                for token in sentence:
                    if token.lemma_ == string:
                        sentence_index.append(i)
                        break  # No need to continue searching this sentence
        return sentence_index
    
    print(string)
    if sentiment == 1:
        file_name = "positive.csv"
    else:
        file_name = "negative.csv"

    # Read CSV file into DataFrame
    df = pd.read_csv(file_name)

    # Access the column containing text data
    text_data = df['text']

    # Find sentences containing the specified word
    sentence_index = find_labels(text_data, string)
    
    # Choose a random sentence index from the list
    random_index = random.choice(sentence_index)

    # Retrieve the text corresponding to the random index
    random_sentence = text_data.iloc[random_index]

    print(random_sentence)
    return random_sentence
