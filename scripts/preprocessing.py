# scripts/preprocessing.py
import spacy
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd

# Ensure 'punkt' tokenizer is available
nltk.download('punkt')
nltk.download('punkt_tab')

# Load SciSpacy's biomedical model
nlp = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words('english'))

# Keywords defined in pubmed_fetch.py
mental_health_terms = ["depression", "bipolar", "PTSD", "anxiety", "suicide"]
epigenetic_terms = ["DNA methylation", "histone modification", "gene expression"]
ethnographic_terms = ["race", "ethnicity", "African American", "Latino", "Caucasian", "Asian", "Native American", "Hispanic", "Indigenous", "Arab", "Middle Eastern"]
socioeconomic_terms = ["socioeconomic status", "income inequality", "poverty", "social class", "education disparity", "economic hardship"]

# Preprocessing function to clean the text
def preprocess_text(abstract):
    abstract = abstract.lower()
    abstract = re.sub(r'\W+', ' ', abstract)
    tokens = word_tokenize(abstract)
    tokens = [token for token in tokens if token not in stop_words]
    doc = nlp(' '.join(tokens))
    lemmatized_tokens = [token.lemma_ for token in doc]
    return lemmatized_tokens

# Function to categorize based on keywords
def categorize_text(text, keywords):
    return ', '.join([keyword for keyword in keywords if keyword.lower() in text.lower()]) or 'None'

# Add new columns to categorize abstracts
def preprocess_abstracts(df):
    df['Processed_Abstract'] = df['Abstract'].apply(preprocess_text)
    
    # Categorize based on predefined terms
    df['Mental_Health_Terms'] = df['Abstract'].apply(lambda x: categorize_text(x, mental_health_terms))
    df['Epigenetic_Terms'] = df['Abstract'].apply(lambda x: categorize_text(x, epigenetic_terms))
    df['Socioeconomic_Terms'] = df['Abstract'].apply(lambda x: categorize_text(x, socioeconomic_terms))
    df['Ethnographic_Terms'] = df['Abstract'].apply(lambda x: categorize_text(x, ethnographic_terms))
    
    return df

if __name__ == "__main__":
    df = pd.read_csv('data/pubmed_articles.csv')
    df = preprocess_abstracts(df)
    df.to_csv('data/preprocessed_pubmed_articles.csv', index=False)
    print("Preprocessing complete and saved to 'data/preprocessed_pubmed_articles.csv'")
