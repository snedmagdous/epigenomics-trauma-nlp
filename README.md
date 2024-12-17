---
# **Epigenomic Impact of Social Trauma: A Meta-Analysis Using NLP** 🚀  

---

## **Team Members and Responsibilities**  

1. **Majd Aldaye (NetID: ma798)**  
   - Debugged `fetch.py` functionality and ensured query reliability.  
   - Developed unit testing frameworks for major scripts (`test_expand_terms.py`, `test_visuals.py`, etc.).  
   - Created and refined visualizations in `myvisuals.py`.  
   - Assisted in debugging and optimizing the `process.py` logic.  

2. **Maya Murry (NetID: mmm443)**  
   - Implemented `expand_terms.py` for dynamic term expansion using semantic similarity.  
   - Developed and optimized `process.py` for text cleaning, tokenization, and categorization.  
   - Designed and tested `run_modeling.py` for generating co-occurrence matrices.  
   - Integrated and ensured smooth execution of `fetch.py` for query-based paper retrieval.  

---

## **Demo Overview**  

The demo will:  
1. Expand search terms using **semantic similarity** techniques.  
2. Fetch relevant papers using dynamically generated **queries**.  
3. Process articles to clean, tokenize, and categorize terms into predefined categories.  
4. Generate **co-occurrence matrices** for deeper relationship analysis.  
5. Visualize insights interactively using heatmaps and 3D scatter plots.  

If any component fails, pre-generated outputs will ensure smooth execution of downstream steps.  

---

## **Preparation**  

### **Environment Setup**  
- Python version: `3.10+`  
- Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  
- Verify the directory structure:  
   - `data/`: Pre-downloaded papers, sample JSON outputs, and mock data.  
   - `scripts/`: Contains all scripts (e.g., preprocessing, modeling, visualizations).  
   - `models/`: (Optional) Saved embeddings/models used during term expansion.  

---

## **Demo Script**  

### **Step 1: Term Expansion (`expand_terms.py`)**  
**Presenter**: Maya  

**Goal**: Expand key terms like "PTSD" and "methylation" using semantic similarity techniques.  

**Steps**:  
1. Run the term expansion script:  
   ```bash  
   python ./scripts/expand_terms.py  
   ```  
2. **Expected Output**:  
   - A JSON file `expanded_terms.json` saved in `data/`.  
   - Contains expanded terms for **mental health**, **epigenetics**, **socioeconomic**, and **ethnicity** categories.  
3. Validate:  
   - Example terms like "methylation" expanded to "DNA methylation," "CpG sites," etc.

---

### **Step 2: Fetching Papers (`fetch.py`)**  
**Presenter**: Majd  

**Goal**: Fetch academic papers based on the expanded queries.  

**Steps**:  
1. Run the fetch script:  
   ```bash  
   python ./scripts/fetch.py  
   ```  
2. **If Automated Fetching Fails**: Run a manual query:  
   ```bash  
   python ./scripts/fetch.py --query "epigenetics AND trauma" --limit 5  
   ```  
3. **Expected Output**:  
   - PDFs of fetched papers saved in `data/papers/`.  

4. Verify:  
   - Files appear in the `data/papers/` directory.  

---

### **Step 3: Preprocessing Articles (`process.py`)**  
**Presenter**: Maya  

**Goal**: Clean, tokenize, and categorize extracted text.  

**Steps**:  
1. Run the preprocessing script:  
   ```bash  
   python ./scripts/process.py  
   ```  
2. **Expected Output**:  
   - A structured JSON file `preprocessed_articles.json` saved in `data/`.  
   - Includes:  
     - **Cleaned text**  
     - **Categorized term counts** (e.g., Mental Health, Epigenetics, Socioeconomic).  

3. Verify JSON Output:  
   - Example: Terms like "PTSD" categorized under **Mental Health**, and "methylation" under **Epigenetics**.  

---

### **Step 4: Term Relationships and Modeling (`run_modeling.py`)**  
**Presenter**: Maya  

**Goal**: Calculate co-occurrence matrices to identify relationships between terms.  

**Steps**:  
1. Run the modeling script:  
   ```bash  
   python ./scripts/run_modeling.py  
   ```  
2. **Expected Output**:  
   - `modeling_output.json` saved in `data/`.  
   - Contains co-occurrence statistics for terms like:  
     - **PTSD and methylation**  
     - **low-income and FKBP5**  

3. Validate Output:  
   - Verify co-occurrence counts for meaningful term pairs.  
NOTE: Without enough CPU space and/or a GPU to run the parallel semantic analysis, this can take extremely long and may crash.
---

### **Step 5: Visualizations (`myvisuals.py`)**  
**Presenter**: Majd  

**Goal**: Visualize relationships using interactive heatmaps and scatter plots.  

**Steps**:  
1. Launch the visualization script:  
   ```bash  
   python ./scripts/myvisuals.py  
   ```  
2. **Expected Output**:  
   - A **Dash server** runs at:  
     ```
     http://127.0.0.1:8050/
     ```  
   - Key Visualizations:  
     - **Heatmaps**:  
       - Socioeconomic terms vs. Epigenetic terms  
       - Ethnicity terms vs. Epigenetic terms  
       - Mental Health terms vs. Epigenetic terms  
     - **3D Scatter Plot**:  
       - Visualize overall relationships among **mental health**, **socioeconomic**, and **epigenetic terms**.  

3. Demonstrate Interactions:  
   - Hover to display term relationships and co-occurrence values.  

---

## **Expected Outputs**  

| Step                | Output File                      | Key Contents                            |  
|---------------------|----------------------------------|----------------------------------------|  
| Term Expansion      | `expanded_terms.json`            | Expanded terms using semantic similarity. |  
| Preprocessing       | `preprocessed_articles.json`     | Cleaned, categorized term counts.      |  
| Modeling            | `modeling_output.json`           | Co-occurrence matrices and term stats. |  
| Visualizations      | Interactive Dash App             | Heatmaps and scatter plots.            |  

---

## **Failsafe Execution**  

If any script fails, the following mock files can be used:  
- `data/expanded_terms.json`  
- `data/preprocessed_articles.json`  
- `data/modeling_output.json`  

These pre-generated files ensure the visualization script can still run.  

---

## **Troubleshooting**  

1. **Fetch Script Fails**: Run queries manually with:  
   ```bash  
   python ./scripts/fetch.py --query "example query" --limit 5  
   ```  
2. **Missing Dependencies**: Ensure all libraries in `requirements.txt` are installed.  
3. **Visualization Errors**: Restart the Dash server:  
   ```bash  
   python ./scripts/myvisuals.py  
   ```  

---
Here is an updated section for the **readme** that provides clear instructions on how to run the test suite. This includes running tests for term expansion, modeling, and visualizations.

---

## **Running the Test Suite**

To ensure the functionality and correctness of each major component in the pipeline, we provide a comprehensive test suite located in the `scripts/tests` directory.

### **Steps to Run the Test Suite**  

1. **Navigate to the Project Root Directory**:  
   Open your terminal or command prompt and ensure you are in the project’s root folder.

   ```bash
   cd <project-root-directory>
   ```

2. **Run All Tests**:  
   Execute all tests using Python's built-in `unittest` module:  

   ```bash
   python -m unittest discover -s scripts/tests
   ```

   This command will search for all test files in the `scripts/tests` directory and run them.

---

### **Individual Tests**  

You can also run specific tests for each script if needed:

1. **Test Term Expansion (`test_expand_terms.py`)**:  
   Verify the logic for dynamically expanding terms and the structure of the output JSON file.

   ```bash
   python -m unittest scripts/tests/test_expand_terms.py
   ```

2. **Test Modeling (`test_modeling.py`)**:  
   Ensure the modeling script correctly categorizes term for co-occurrence calculation and produces the expected output format.

   ```bash
   python -m unittest scripts/tests/test_modeling.py
   ```

3. **Test Visualizations (`test_visuals.py`)**:  
   Confirm that visualizations, such as heatmaps and scatter plots, are generated successfully and without errors.

   ```bash
   python -m unittest scripts/tests/test_visuals.py
   ```

---

### **Expected Output**  
For each test suite, you will see results similar to the following:  

```
......
----------------------------------------------------------------------
Ran 6 tests in 0.123s

OK
```

If a test fails, it will show the specific error and traceback, which you can use to debug the issue.

---

### **Debugging Test Failures**  
- Ensure all dependencies are installed from `requirements.txt`:  
   ```bash
   pip install -r requirements.txt
   ```
- Check the paths to your input/output files and directories, as some tests rely on sample data in `data/` and `scripts/`.  

---

By following these steps, you can verify that each pipeline component (term expansion, preprocessing, modeling, and visualizations) works as intended and produces correct outputs.

## **Closing Notes**  

- **Majd**: Demonstrated preprocessing and visualizations.  
- **Maya**: Showed term expansion, data fetching, and modeling.  

This pipeline demonstrates the power of NLP in analyzing the intersection of trauma, mental health, and epigenetics, offering meaningful insights for further study.
