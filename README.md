---

# CAP_Epigenomics-Analysis_ma798_mmm443  🚀

## **Demo Script for Epigenomic NLP Project**  

### **Team Members and Responsibilities**  
1. **Majd Aldaye (NetID: ma798)**  
   - Debugged `fetch.py` functionality extensively and ensured query reliability.  
   - Developed unit testing frameworks for major scripts (`test_expand_terms.py`, `test_visuals.py`, etc.).  
   - Created and refined visualizations in `myvisuals.py`.  
   - Assisted in debugging and optimizing the `process.py` logic.  

2. **Maya Murry (NetID: mmm443)**  
   - Implemented `expand_terms.py` for term expansion using semantic similarity.  
   - Developed and optimized `process.py` for text cleaning, tokenization, and term categorization.  
   - Designed and tested the `run_modeling.py` script for co-occurrence matrix calculations.  
   - Integrated `fetch.py` and ensured smooth query-based paper fetching.  

---

## **Demo Overview**  

The demo will:  
1. Run the **term expansion** logic to dynamically expand terms.  
2. Fetch research papers using **queries**.  
3. Process articles by cleaning, categorizing terms, and creating structured outputs.  
4. Run the modeling pipeline to calculate term co-occurrences.  
5. Visualize relationships between terms using interactive heatmaps and scatter plots.  

If any component fails during the demo, pre-generated files will be provided to ensure continuity.  

---

## **Preparation**  

1. **Environment Setup**:  
   - Python version: `3.10+`  
   - Install all dependencies:  
     ```bash  
     pip install -r requirements.txt  
     ```  
   - Ensure the following directories/files exist:  
     - `data/`: Contains pre-downloaded papers, sample outputs, and mock data.  
     - `scripts/`: Contains all major pipeline scripts and utilities.  
     - `models/`: (Optional) Contains embeddings or saved models.  

2. **Data Preparation**:  
   - Place input research papers into `data/papers/`.  
   - Ensure any pre-generated files (e.g., `expanded_terms.json`, `preprocessed_articles.json`) are available for failsafe execution.  

---

## **Demo Script**  

### **Step 1: Term Expansion (`expand_terms.py`)**  
**Presenter**: Maya  
**What to Show**:  
- Running the term expansion script to generate semantically similar terms.  

**Steps**:  
1. Run the term expansion script:  
   ```bash  
   python ./scripts/expand_terms.py  
   ```  
   - Expected Output:  
     - A JSON file `expanded_terms.json` will be saved in the `data/` folder.  
     - Displayed expanded terms for categories like Mental Health, Epigenetics, and Socioeconomic terms.  

2. If there’s an issue, validate the JSON structure manually:  
   - Confirm valid expansions of seed terms based on Wikipedia and semantic similarity.  

---

### **Step 2: Fetching Papers (`fetch.py`)**  
**Presenter**: Majd  
**What to Show**:  
- Running the script to fetch papers using queries.  

**Steps**:  
1. Run the fetch script:  
   ```bash  
   python ./scripts/fetch.py  
   ```  
   - If stuck, **manually run a query** in the terminal:  
     ```bash  
     python ./scripts/fetch.py --query "epigenetics AND mental health" --limit 5  
     ```  
   - Example Output:  
     - Papers saved in the `data/papers/` directory as PDFs or text files.  

2. Confirm the downloaded papers:  
   - Ensure files are successfully saved in `data/papers/`.  

---

### **Step 3: Preprocessing Articles (`process.py`)**  
**Presenter**: Maya  
**What to Show**:  
- Running the preprocessing script to clean text, categorize terms, and prepare the data for modeling.  

**Steps**:  
1. Run the preprocessing script:  
   ```bash  
   python ./scripts/process.py  
   ```  
   - Expected Output:  
     - A structured JSON file `preprocessed_articles.json` saved in the `data/` folder.  
   - Key Features:  
     - Cleaned text  
     - Categorized term counts (e.g., mental health terms, epigenetic terms).  

2. Validate the JSON output:  
   - Each article should contain `paper_name`, categorized term counts, and disparity metadata.  

---

### **Step 4: Modeling (`run_modeling.py`)**  
**Presenter**: Maya  
**What to Show**:  
- Generating term co-occurrence matrices and summarizing key relationships.  

**Steps**:  
1. Run the modeling script:  
   ```bash  
   python ./scripts/run_modeling.py  
   ```  
   - Expected Output:  
     - `modeling_output.json` saved in the `data/` folder.  
     - This file will contain categorized term counts and co-occurrence matrices per article.  

2. Validate the modeling output:  
   - Confirm co-occurrence counts for terms like `PTSD` with `methylation` or `low-income`.  

---

### **Step 5: Visualizations (`myvisuals.py`)**  
**Presenter**: Majd  
**What to Show**:  
- Interactive visualizations of term relationships.  

**Steps**:  
1. Launch the visualization app:  
   ```bash  
   python ./scripts/myvisuals.py  
   ```  
   - Expected Output:  
     - A **Dash server** will open at `http://127.0.0.1:8050/`.  
     - Visualizations include:  
       - Heatmaps showing relationships between **Epigenetic** terms and **Mental Health**/Socioeconomic/Ethnicity terms.  
       - A 3D scatter plot for high-level term associations.  

2. Key Interactions to Showcase:  
   - Hover over heatmap cells to view specific co-occurrence counts.  
   - Explore patterns in the data, e.g., high co-occurrences for marginalized groups or low-income terms.  

---

## **Expected Outputs**  

### Key Files Generated:  
- `expanded_terms.json`: Semantically expanded terms.  
- `preprocessed_articles.json`: Cleaned and categorized article data.  
- `modeling_output.json`: Co-occurrence matrices for categorized terms.  

### Interactive Dash Visualizations:  
- Accessible at `http://127.0.0.1:8050/`.  

---

## **Failsafe Execution**  

If any script fails, the following mock files are available for use:  
- `data/expanded_terms.json`  
- `data/preprocessed_articles.json`  
- `data/modeling_output.json`  

These ensure smooth execution of downstream steps.  

---

## **Troubleshooting**  

1. **Fetch Script Fails**:  
   - Run manually with a specific query using `--query` and `--limit` options.  

2. **Term Expansion Issues**:  
   - Check for internet connectivity (necessary for Wikipedia API).  

3. **Visualizations Not Loading**:  
   - Ensure all dependencies in `requirements.txt` are installed.  
   - Re-run the server script:  
     ```bash  
     python ./scripts/myvisuals.py  
     ```  

---