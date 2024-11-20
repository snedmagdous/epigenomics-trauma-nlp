import os
import re
import json
import logging
import fitz  # PyMuPDF for PDF text extraction
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download
from collections import defaultdict, Counter
import spacy

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Download NLTK dependencies
download("punkt")
download("stopwords")

# Load SciSpacy's biomedical model
nlp = spacy.load("en_core_sci_lg")

# Stopwords
stop_words = set(stopwords.words("english"))

# Paths and directories
RAW_ARTICLES_DIR = "./data/papers"  # Directory with raw text or PDFs
TOP_TERMS_FILE = "./data/expanded_terms/top_similar_terms.json"  # Terms from fetch.py
PROCESSED_DATA_FILE = "./data/processed/preprocessed_articles.json"

# Load expanded terms (core + similar terms)
with open(TOP_TERMS_FILE, "r", encoding="utf-8") as file:
    expanded_terms = json.load(file)


def extract_pdf_content(pdf_directory):
    """
    Extract text from PDF files in a directory.
    Args:
        pdf_directory (str): Directory containing PDF files.
    Returns:
        list: List of dictionaries with file names and extracted content.
    """
    pdf_data = []
    for file_name in os.listdir(pdf_directory):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(pdf_directory, file_name)
            logging.info(f"Extracting content from: {file_name}")
            try:
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                pdf_data.append({"file_name": file_name, "content": text.strip()})
            except Exception as e:
                logging.error(f"Error extracting {file_name}: {e}")
    return pdf_data


def clean_text(text):
    """
    Perform basic text cleaning and tokenization.
    Args:
        text (str): Raw text to clean.
    Returns:
        str: Cleaned text.
    """
    text = re.sub(r"[^\w\s]", " ", text.lower())  # Lowercase and remove special characters
    return text


def lemmatize_and_process(text):
    """
    Lemmatize text using SciSpacy and preserve biomedical entities.
    Args:
        text (str): Cleaned text to process.
    Returns:
        list: Lemmatized tokens.
    """
    doc = nlp(text)
    lemmatized_tokens = []
    for token in doc:
        if token.text in expanded_terms.get("Epigenetic Terms", []):  # Preserve key terms
            lemmatized_tokens.append(token.text)
        elif token.ent_type_ in ["GENE_OR_GENE_PRODUCT", "DISEASE", "CHEMICAL"]:
            lemmatized_tokens.append(token.text)
        else:
            lemmatized_tokens.append(token.lemma_)
    return lemmatized_tokens


def save_sample_results_to_file(tokens, file_path="sample_output.txt", doc=None):
    """
    Save sample tokens and named entities to a file for debugging.
    Args:
        tokens (list): List of tokens.
        file_path (str): Path to the output file.
        doc (spacy.Doc): Processed SciSpacy document (optional).
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Sample Results from Tokenization and Named Entity Recognition:\n")
        f.write("=" * 50 + "\n")
        f.write("Tokens:\n")
        f.write(", ".join(tokens[:50]) + "\n\n")
        if doc:
            f.write("Named Entities:\n")
            for ent in doc.ents:
                f.write(f"Entity: {ent.text}, Type: {ent.label_}\n")


def categorize_and_count_terms(text, expanded_terms):
    """
    Categorize text using expanded terms and count term frequencies.
    Args:
        text (str): Processed text to analyze.
        expanded_terms (dict): Dictionary of core terms and their expanded similar terms.
    Returns:
        dict: Term counts for each category.
    """
    term_counts = {category: Counter() for category in expanded_terms.keys()}
    text_tokens = text.split()
    for category, terms in expanded_terms.items():
        term_counts[category] = Counter(
            term for term in terms if term.lower() in map(str.lower, text_tokens)
        )
    return {category: dict(counts) for category, counts in term_counts.items()}


def preprocess_articles(input_dir=RAW_ARTICLES_DIR, expanded_terms=expanded_terms):
    """
    Process raw articles (text or PDFs) to clean, categorize, and calculate statistics.
    Args:
        input_dir (str): Directory containing raw articles.
        expanded_terms (dict): Dictionary with core terms and expanded similar terms.
    Returns:
        list: List of processed article metadata.
    """
    processed_data = []

    # Extract content from PDFs or text files
    articles = extract_pdf_content(input_dir) if input_dir.endswith(".pdf") else [{"file_name": f, "content": open(os.path.join(input_dir, f), "r").read()} for f in os.listdir(input_dir)]

    for article in articles:
        raw_text = article["content"]
        cleaned_text = clean_text(raw_text)
        tokens = lemmatize_and_process(cleaned_text)
        term_counts = categorize_and_count_terms(" ".join(tokens), expanded_terms)

        # Save metadata
        article_metadata = {
            "paper_name": article["file_name"],
            "cleaned_text": " ".join(tokens),
            "term_counts": term_counts,
        }
        processed_data.append(article_metadata)

    # Save processed data to JSON
    with open(PROCESSED_DATA_FILE, "w", encoding="utf-8") as json_file:
        json.dump(processed_data, json_file, indent=4)
    logging.info(f"Processed data saved to {PROCESSED_DATA_FILE}")

    return processed_data


if __name__ == "__main__":
    processed_articles = preprocess_articles()
    logging.info(f"Processed {len(processed_articles)} articles successfully.")
