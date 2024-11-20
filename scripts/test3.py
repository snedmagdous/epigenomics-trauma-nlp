# Import necessary libraries
import spacy
from spacy.matcher import PhraseMatcher
from nltk.corpus import wordnet
from pypdf import PdfReader

# Ensure NLTK's WordNet is downloaded
import nltk
nltk.download('wordnet')

# Step 1: Function to Fetch Mental Health Terms from WordNet
def get_mental_health_terms():
    """
    Dynamically fetch mental health-related terms using WordNet.
    
    Returns:
        list: A list of mental health condition names and synonyms.
    """
    # Define a base term to search around
    base_terms = ["mental disorder", "mental illness", "psychological disorder"]
    terms = set()

    for base_term in base_terms:
        synsets = wordnet.synsets(base_term)
        for synset in synsets:
            # Add synonyms
            terms.update([lemma.name().replace('_', ' ') for lemma in synset.lemmas()])
            # Add hypernyms (broader terms)
            for hypernym in synset.hypernyms():
                terms.update([lemma.name().replace('_', ' ') for lemma in hypernym.lemmas()])
            # Add hyponyms (narrower terms)
            for hyponym in synset.hyponyms():
                terms.update([lemma.name().replace('_', ' ') for lemma in hyponym.lemmas()])
    return list(terms)

# Step 2: Function to Extract Mental Health Terms from Text
def extract_mental_health_conditions(text, terms):
    """
    Extract mental health terms from the text dynamically.
    
    Args:
        text (str): Input text.
        terms (list): List of mental health terms.
    
    Returns:
        list: Extracted terms present in the text.
    """
    # Load spaCy language model
    nlp = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab)
    
    # Create patterns from the list of terms
    patterns = [nlp.make_doc(term) for term in terms]
    matcher.add("MentalHealthConditions", patterns)

    # Process the input text
    doc = nlp(text)
    matches = matcher(doc)
    
    # Extract matched terms
    return [doc[start:end].text for _, start, end in matches]

# Step 3: Main Script to Fetch Terms and Perform Extraction
if __name__ == "__main__":
    # Fetch mental health terms dynamically
    mental_health_terms = get_mental_health_terms()
    print(f"Fetched Mental Health Terms ({len(mental_health_terms)}):")
    print(mental_health_terms[:10])  # Print a sample of terms for validation

    # Example text to analyze
    example_text = """
    The patient was diagnosed with anxiety, bipolar disorder, and PTSD. They also mentioned symptoms of depression 
    and occasional panic attacks, but ruled out schizophrenia.
    """
    path = 'data\papers\An epigenetic mechanism links socioeconomic status to changes in depression-related brain function in high-risk adolescents.pdf'
    reader = PdfReader(path)
    example_pdf = ''
    with open('pdf2.txt', 'w', encoding='UTF-8') as f:
      for page in reader.pages:
          example_pdf += page.extract_text()  

    # Extract mental health conditions from the example text
    extracted_conditions = extract_mental_health_conditions(example_text, mental_health_terms)
    extracted_conditions2 = extract_mental_health_conditions(example_pdf, mental_health_terms)
    print("\nExtracted Mental Health Conditions:")
    print(extracted_conditions)
    print("\nExtracted Mental Health Conditions 2:")
    print(extracted_conditions2)

