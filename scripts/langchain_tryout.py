import os
from pypdf import PdfReader
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# Directory containing PDF papers
DATA_DIR = "./data/testing_folder"

# Load SpaCy's NER model
import spacy

nlp = spacy.load("en_core_web_sm")  # Load a pre-trained NER model

# Define a function to extract text from a PDF
def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using pypdf."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

# Define a function to extract entities using NER
def extract_entities_with_ner(text):
    """
    Extract entities related to mental health using NER.
    Returns a list of identified terms and their labels.
    """
    doc = nlp(text)
    terms = []
    for ent in doc.ents:
        if ent.label_ in ["DISEASE", "MENTAL_CONDITION"]:  # Adjust based on NER model
            terms.append((ent.text, ent.label_))
    return terms

def extract_terms_from_papers(data_dir):
    """
    Extract mental health terms from all PDF papers in the directory.
    Returns a dictionary mapping file names to extracted terms.
    """
    results = {}
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(data_dir, file_name)
            print(f"Processing file: {file_name}")
            
            # Extract text and apply NER
            text = extract_text_from_pdf(file_path)
            entities = extract_entities_with_ner(text)
            results[file_name] = entities
    return results

if __name__ == "__main__":
    # Extract terms from all PDF files
    term_results = extract_terms_from_papers(DATA_DIR)

    # Display the results
    for file_name, entities in term_results.items():
        print(f"\nResults for {file_name}:")
        for term, label in entities:
            print(f"  {term} ({label})")
