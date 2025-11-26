# Assignment 01: Cluster Analysis on Gene Expression
(CPBS 7602: Introduction to Big Data in the Biomedical Sciences)  
By Milton Pividori  
Department of Biomedical Informatics  
University of Colorado Anschutz Medical Campus

### Assignment Overview
Students will download a subset of the GTEx gene expression dataset (https://gtexportal.org/home/) and apply different clustering methods to explore whether clusters can identify the tissue of origin. This assignment will reinforce concepts in clustering, practical data handling, and biological interpretation of clusters.

**Due:** December 2, 2025 at 5 pm MT

### Reading Material (Optional)
• Ben Heil et al. *The Effect of Non-linear Signal in Classification Problems Using Gene Expression.* PLOS Computational Biology. https://doi.org/10.1371/journal.pcbi.1010984  
  ◦ They used GTEx gene expression to predict the tissue of origin and sex. Although we are not predicting in this assignment, it's helpful to see how they processed the GTEx data and obtained the labels for the samples.

---

## Assignment Tasks

### 1. Data Download and Preprocessing

1. Go to the [GTEx portal](https://gtexportal.org/home/) → **Downloads → Open Access Data → Bulk Tissue Expression**.  
   Use **GTEx Analysis v8**. Download the **“Gene TPMs”** file.

   **Notes:**
   1. Skip the top 2 rows (header) when reading with Pandas.  
   2. **Rows:** one gene per row. The `Gene Ensembl ID` (starts with `ENSG`) and `Description` (gene symbol).  
   3. **Columns:** one sample per column (`GTEX-...`).  
   4. Values are **TPM** (transcripts per million).

2. Download the **sample attributes** `.txt` file from the **Metadata** tab.

   **Notes:**
   1. Rows = samples; columns = metadata fields.  
   2. Use the **simplified tissue column**. Example: `GTEX-1117F-0003-SM-58Q7G` → *Blood*.

3. Create a working subset:

   1. From metadata: select the **top 10 tissues** with the largest sample size.  
   2. From the gene expression file: select the **top 5,000 most variable genes**.  
   3. Be mindful of memory usage when using `.var()` — consider efficient `.read_csv` usage.  
   4. If needed, reduce sample or gene count (using the same logic).  

4. Generate a unified dataset with:
   - **Inputs:** samples from top tissues, represented by genes  
   - **Targets:** tissue labels  

5. Standardize the input data.

---

### 2. Cluster Analysis

1. Perform clustering to determine whether samples group according to tissue of origin.  
2. Use **at least two different clustering methods**.  
3. Explore **different parameters** for each method.

---

### 3. Cluster Evaluation and Interpretation

1. Using **external metrics**, assess how well clusters match true tissue labels.  
2. Using **internal metrics**, assess cluster quality.  
3. Identify **important genes (features)** driving clustering. Explain your approach.  
4. Identify important genes **per tissue**. Explain your approach.

---

## Assignment Deliverables

### Code

Submit code via a **GitHub repository** with a folder named `assignment01`.

The code should include:

- A `README.md` with:
  - instructions to reproduce results  
  - instructions to create the conda environment  

- Well-documented **Jupyter notebooks** covering all steps  
  ◦ You may use intermediate files between steps.  

- Random seeds must be set for reproducibility (e.g., using `numpy.random.seed()`).

---

## Analysis Report

- No page limit.  
- Clearly annotate your work.

---

## Grading Rubric

**• Data Preprocessing and Standardization (20%)**  
  Handling of data preparation, standardization, and code clarity.

**• Clustering Implementation (30%)**  
  Correct application of clustering algorithms, including parameter exploration.

**• Evaluation and Comparison (30%)**  
  Use of evaluation metrics, visualizations, and accurate comparisons with tissues.

**• Interpretation and Reporting (20%)**  
  Quality of explanations, understanding, and completeness of the report.
