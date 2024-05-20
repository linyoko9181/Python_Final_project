import pandas as pd
import spacy
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


# Check if CUDA is available
if torch.cuda.is_available():
    # Set the GPU device to use
    device = torch.device("cuda:0")  # Assuming you want to use the first GPU
    print("Using CUDA device:", torch.cuda.get_device_name(device))
else:
    print("CUDA is not available, using CPU")

def preprocess_data():
    # read the csv file
    csv_path = 'C:\\Users\\yanso\\Documents\\FinalProject\\original_code/reviews.csv'
    df = pd.read_csv(csv_path)
    # delete additonal columns
    columns_to_drop_indices = [3,4,7,8,9,10,11]
    df.drop(df.columns[columns_to_drop_indices], inplace=True, axis=1)
    # change the name of the columns
    new_column_names = ['User Photo', 'User Name', 'Rank', 'Time', 'text']
    df.columns = new_column_names
    # delete not useful text: nonascii and emtpy columns
    df = df[df['text'].astype(str).map(lambda x: x.isascii())]
    df = df.dropna()
    #download the file 
    csv_path = 'Data.csv'
    df.to_csv(csv_path, index=False)
    return df

def sentiment_score(review, device):
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment').to(device)
    tokens = tokenizer.encode(review, return_tensors='pt').to(device)
    result = model(tokens)
    return int(torch.argmax(result.logits))+1

reviews = preprocess_data()

#get the sentiment score 
reviews['sentiment'] = reviews['text'].apply(lambda x: sentiment_score(x[:512], device))
sentiment_avg = reviews['sentiment'].mean()
print(f"rating:{sentiment_avg}")

#create positive reviews dataframe and negative reviews dataframe
positive = reviews[reviews['sentiment']>3].copy()
negative = reviews[reviews['sentiment']<3].copy()
positive.to_csv('positive.csv', index=False)
negative.to_csv('negative.csv', index=False)