from pypdf import PdfReader
import pytesseract
from PIL import Image
import re
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

def extract_text_from_pdf(pdf_path, use_ocr=False):
    """
    Extracts text from a PDF. Optionally applies OCR for scanned PDFs.
    """
    extracted_text = []
    try:
        pdf = PdfReader(pdf_path)
        for page in pdf.pages:
            text = page.extract_text()
            if not text and use_ocr:  # If no text is found, use OCR
                with open('images.txt', 'w') as f:
                    image = page.to_image().original
                    text = pytesseract.image_to_string(Image.fromarray(image))
                    print(text, file=f)
            if text:
                extracted_text.append(text)
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return "\n".join(extracted_text)

def preprocess_text(text):
    """
    Preprocesses extracted text: removes noise, normalizes, and cleans.
    """
    print('Start preprocessing...')
    try:
        text = re.sub(r"\[\d+\]", "", text)  # Remove references like [1], [2]
        text = re.sub(r'\b[\d+]\b', '', text)  # Remove numbers
        text = re.sub(r'\b\w{1,2}\b', '', text)  # Remove short words (length 1-2)
        text = re.sub(r"\b\w*doi\w*\b", '', text)  # Remove DOIs
        text = re.sub(r"http\S+", '', text)  # Remove links
        text = re.sub(r"\s+", " ", text)  # Normalize whitespace
        text = re.sub(r"[^a-zA-Z\s.,-]", "", text)  # Keep only valid characters
    except Exception as e:
        print(f"Error during preprocessing: {e}")
    print('Preprocessing complete.')
    return text.lower()  # Convert to lowercase

def infer_categories_with_lda(text, num_topics=5, num_top_words=10):
    """
    Infers categories from text using LDA topic modeling.
    """
    vectorizer = CountVectorizer(stop_words="english", max_features=5000)
    dt_matrix = vectorizer.fit_transform([text])
    
    lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda_model.fit(dt_matrix)
    
    terms = vectorizer.get_feature_names_out()
    categories = []
    for topic in lda_model.components_:
        topic_terms = [terms[i] for i in topic.argsort()[-num_top_words:]]
        categories.extend(topic_terms)
    return list(set(categories))

def infer_categories_with_clustering(text, num_clusters=5):
    """
    Infers categories from text using embedding-based clustering.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    words = list(set(text.split()))
    embeddings = model.encode(words)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(embeddings)
    
    clusters = {i: [] for i in range(num_clusters)}
    for idx, label in enumerate(kmeans.labels_):
        clusters[label].append(words[idx])
    
    categories = [cluster[0] for cluster in clusters.values() if cluster]
    return categories

def process_pdf_directory(directory_path, limit, use_ocr=False):
    """
    Processes all PDFs in a directory, extracts text, preprocesses it, 
    and combines for analysis.
    """
    combined_text = ""
    counter = 0

    for filename in os.listdir(directory_path):
        if counter >= limit:
            break
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".pdf"):
            print(f"Processing file: {filename}")
            text = extract_text_from_pdf(file_path, use_ocr=use_ocr)
            if text:
                combined_text += preprocess_text(text) + "\n"
                counter += 1
            else:
                print(f"Warning: No text extracted from {filename}")
    return combined_text

# Main script
if __name__ == "__main__":
    # Directory containing PDFs
    pdf_directory = './data/papers'

    # Process PDFs and combine text
    combined_text = process_pdf_directory(pdf_directory, limit=100)

    if combined_text.strip():
        # Using LDA
        categories_lda = infer_categories_with_lda(combined_text)
        print("\nCategories (LDA):", categories_lda)

        # Using Clustering
        categories_clustering = infer_categories_with_clustering(combined_text)
        print("\nCategories (Clustering):", categories_clustering)
    else:
        print("No text extracted from the provided PDFs.")
    # path = 'data\papers\An epigenetic mechanism links socioeconomic status to changes in depression-related brain function in high-risk adolescents.pdf'
    # reader = PdfReader(path)
    # with open('pdf2.txt', 'w', encoding='UTF-8') as f:
    #   for page in reader.pages:
    #       print(preprocess_text(page.extract_text()), file=f)