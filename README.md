# CAP_Epigenomics-Analysis_ma798_mmm443

# Demo Script for Epigenomic NLP Project

## **Team Members and Responsibilities**
1. **Majd Aldaye (NetID: ma798)**  
   Contributions:
   - Implemented testing frameworks for all major scripts (`test_expand_terms.py`, `test_visuals.py`, etc.).
   - Debugged `fetch.py` and `expand_terms.py` functionality extensively.
   - Worked on developing visualization logic in `myvisuals.py`.
   - Assisted in refining preprocessing logic (`process.py`) and improving co-occurrence calculations.

2. **Maya Murry (NetID: mmm443)**  
   Contributions:
   - Implemented `fetch.py` for querying and downloading research papers.
   - Developed term expansion using semantic similarity in `expand_terms.py`.
   - Refactored `process.py` for improved text cleaning, tokenization, and categorization.
   - Began implementing `topic_modeling.py` using LangChain for deeper semantic analysis.

---

## **Demo Goals**
The demo will:
1. Verify  major components of the pipeline run successfully against test cases.
2. Showcase distinct contributions from each team member.
3. Provide clear and reproducible steps for the TA to run the demo independently.

---

## **Demo Overview**

### **Preparation**
1. **Environment Setup**:
   - Python version: `3.10+`
   - Dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Ensure the following directories/files exist:
     - `data/`: Contains sample papers, mock JSON outputs, and intermediate files.
     - `scripts/`: Contains all major pipeline scripts and test suites.
     - `tests/`: Contains unit tests for key components.
     - `models/`: Contains different models that get produced and used throughout the pipeline.

2. **Data Preparation**:
   - Data for testing is located in `data/papers/`.
   - A pre-generated expanded terms JSON file (`expanded_terms.json`) and sample preprocessed output (`preprocessed_articles.json`) are included in .

3. **Execution Plan**:
   - The demo will run on **both laptops** for efficiency, each prioritizing certain code to run.
   - Code components will be run sequentially.

---

## **Demo Script**
### **Step 1: Term Expansion (`expand_terms.py`)**  
**Presenter**: Maya 
**What to Show**:  
- Running the term expansion logic to dynamically generate expanded terms based on semantic similarity.
- Testing the term expansion functionality with a unit test.

**Steps**:  
1. Run the term expansion script:
   ```bash
   python ./scripts/expand_terms.py
   ```
   - Expected output: `expanded_terms.json` saved in the `scripts/` directory.  
   - Key terms like `Mental Health`, `Epigenetics`, and `Ethnographic Terms` should have their related terms expanded and displayed in the terminal.

2. Run unit tests:
**Presenter**: Majd
   ```bash
   python -m unittest tests/test_expand_terms.py
   ```
   - Expected result: All test cases pass, verifying the logic for term generation, filtering invalid Wikipedia titles, and JSON structure.

---
### **Step 2: Fetching Papers (`fetch.py`)**  
**Presenter**: Majd   
**What to Show**:  
- Running the query-building logic and downloading papers using a mock query for efficiency.

**Steps**:  
1. Generate a query:
   ```bash
   python ./scripts/fetch.py
   ```
   - Expected output: A sample query displayed in the terminal.
   - Mock results: Pre-downloaded papers saved in `data/papers/`.

2. Validate the fetched papers directory:
   - Check that PDFs and metadata files are stored correctly in `data/papers/`.

---

### **Step 3: Preprocessing Articles (`process.py`)**  
**Presenter**: Maya  
**What to Show**:  
- Running the preprocessing script to clean, tokenize, and categorize text.
- Verifying outputs with processed JSON files and co-occurrence matrices.

**Steps**:  
1. Run the preprocessing script:
   ```bash
   python ./scripts/process.py
   ```
   - Expected output: `preprocessed_articles.json` saved in the `data/` directory.
   - Key features: Cleaned text, term counts, and disparity metadata (e.g., ethnicity, socioeconomic status).

2. Check the co-occurrence matrix in the JSON output:
   - Verify that relationships between terms are calculated correctly.

3. Run unit tests:
**Presenter**: Majd 
   ```bash
   python -m unittest scripts.tests.test_expand_terms
   ```
   - Expected result: Expected test cases pass, understanding the ones that fail, ensuring the integrity of text cleaning, tokenization, and categorization logic.

---

### **Step 4: Topic Modeling (`topic_modeling.py`)**  
**Presenter**: Maya Murry  
**What to Show**:  
- A preliminary LangChain-based topic modeling implementation to identify themes.

**Steps**:  
1. Run the topic modeling script:
   ```bash
   python ./scripts/topic_modeling.py
   ```
   - Expected output: A JSON file (`postprocessed_articles.json`) with identified topics for sample articles.

2. Display the topics:
   - Show key themes extracted from the preprocessed data.

---

### **Step 5: Visualizations (`myvisuals.py`)**  
**Presenter**: Majd
**What to Show**:  
- Generating interactive visualizations (e.g., heatmaps, 3D scatter plots) to represent relationships.

**Steps**:  
1. Launch the app:
   ```bash
   python ./scripts/myvisuals.py
   ```
   - Expected output: A browser window displaying:
     - Heatmaps of term frequencies across categories.
     - 3D scatter plots showing relationships between terms.

2. Explain the interactive features:
   - Highlight how users can explore term relationships visually.
   - Elaborate on next implementation steps of 3D dash interactions, chatbot integration to interpret results, and better results after topic_modeling completiob.

---

## **What the TA Should Expect**
- **Output Files**:
  - `expanded_terms.json`: Expanded terms generated dynamically.
  - `preprocessed_articles.json`: Cleaned and categorized article data that will then be used by topic_modeling to further interpret data.
- **Interactive Visuals**: A running app with multiple visualization types.
- **Successful Test Cases**: Verified correctness of each pipeline step.

---

## **Failsafe**
- If any component fails, mock data and pre-generated outputs will be used to demonstrate the downstream steps.
- Mock files:
  - `./expanded_terms.json`
  - `./preprocessed_articles.json`

This script ensures smooth, reproducible execution of the demo while showcasing significant contributions from both team members.
