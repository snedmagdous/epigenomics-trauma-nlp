"""
fetch.py 

Purpose:
- Fetches and expands terms related to predefined categories (e.g., Mental Health, Epigenetic, etc.) 
  using semantic similarity.
- Dynamically generates a list of top similar terms for each core term in the categories, 
  enabling enhanced text analysis for the next step in preprocessing.py.

Key Steps:
1. Load core terms for categories like Mental Health, Epigenetic, Ethnographic, and Socioeconomic terms.
2. Use a SentenceTransformer model to calculate semantic similarity between core terms and a corpus 
   (e.g., Wikipedia, other text datasets).
3. Generate a list of top similar terms for each core term.
4. Save the expanded terms for each category in a structured JSON file.

Inputs:
- Core term lists for categories (e.g., ["depression", "anxiety", "PTSD"] for Mental Health).
- Corpus of potential related terms (e.g., scraped Wikipedia links or other text data).

Outputs:
- JSON file (`top_similar_terms.json`) containing:
  {
      "Mental Health Terms": {"depression": ["stress", "psychosis", ...], ...},
      "Epigenetic Terms": {"methylation": ["CpG islands", "DNA modifications", ...], ...},
      ...
  }

How to Use:
- This script generates a JSON file of expanded terms, which is consumed by `preprocessing.py` for term matching.
"""

import numpy as np
import logging, random
import subprocess
import os
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_query(path_to_file, repetitions=2):
    """
    Generate a query ensuring at least a minimum number of terms from each category.

    Args:
        path_to_file (str): Path to the JSON file with expanded terms.
        min_terms (int): Minimum number of terms from each category to be included in the query.

    Returns:
        str: Generated query string.
    """
    try:
        with open(path_to_file, 'r', encoding='utf-8') as file:
            expanded_terms = json.load(file)
    except FileNotFoundError:
        logging.error(f"Error: The file at {path_to_file} was not found.")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error: Failed to decode JSON file at {path_to_file}. Details: {e}")
        raise

    # Flatten nested Ethnographic Terms into a single list of terms
    ethnographic_flattened = [
        term for category_terms in expanded_terms["Ethnographic Terms"].values()
        for term in category_terms
    ]

    # Helper function to generate shuffled queries
    def generate_shuffled_queries(terms, repetitions):
        combined_lists = []
        for lst in terms:
            combined_lists += lst
        shuffled_queries = []
        for _ in range(repetitions):
            shuffled_terms = combined_lists[:]
            random.shuffle(shuffled_terms)
            shuffled_queries.append(f"({' OR '.join(shuffled_terms)})")
        return " AND ".join(shuffled_queries)
    
    # Generate subqueries
    epigenetic_query = generate_shuffled_queries(list(expanded_terms["Epigenetic Terms"].values()), repetitions)
    mental_health_query = generate_shuffled_queries(list(expanded_terms["Mental Health Terms"].values()), repetitions)
    ethnographic_query = generate_shuffled_queries(list(expanded_terms['Ethnographic Terms']), repetitions)
    socioeconomic_query = generate_shuffled_queries(list(expanded_terms["Socioeconomic Terms"].values()), repetitions)

    # Combine all subqueries
    query = (
        f"{epigenetic_query} AND "
        f"{mental_health_query} AND "
        f"{ethnographic_query} AND "
        f"{socioeconomic_query}"
    )

    logging.info(f"Generated Query: {query}")
    return query


def fetch_papers(query, scholar_pages=1, min_year=2000, sort_by_relevance=True, output_dir="./data/papers"):
    """
    Fetch academic papers using PyPaperBot based on the generated query.

    Args:
        query (str): Query string for searching papers.
        scholar_pages (int): Number of Google Scholar pages to scrape.
        min_year (int): Minimum publication year for papers.
        sort_by_relevance (bool): If True, fetch papers sorted by relevance instead of recency.
        output_dir (str): Directory to save downloaded papers.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Add sorting preference to the query
    sort_option = "--sort-relevance" if sort_by_relevance else "--sort-recency"

    # Construct PyPaperBot command
    command = [
        "python", "-m", "PyPaperBot",
        f"--query={query}",
        f"--scholar-pages={scholar_pages}",
        f"--min-year={min_year}",
        f"--dwn-dir={output_dir}",
        sort_option
    ]

    try:
        subprocess.run(command, check=True)
        logging.info(f"Papers successfully fetched and saved to {output_dir}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error fetching papers with PyPaperBot: {e}")

if __name__ == "__main__":
    # Path to the expanded terms JSON file
    path_to_file = "./scripts/expanded_terms.json"

    # Generate the query ensuring at least 5 terms per category
    query = generate_query(path_to_file)

    # Fetch papers using the generated query, sorted by relevance
    fetch_papers(query, scholar_pages=1, min_year=2000, sort_by_relevance=True)