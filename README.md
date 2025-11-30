# Assignment 1 

This assignment explores multiple clustering algorithms on bulk gene counts from ten tissues. 
Look at [assignment-description.md](assignment-description.md) for more detail.

## Set up 
Download dependencies with `conda env create -f environment.yml`. 
(this file was created with `conda env export --from-history > environment.yml`)


## Analysis
Run these [scripts](src/py/) in numerical order to reproduce results. 

#### `001-download-data`
- Download gene counts matrix and sample/subject metadata and format in summarized experiment format. 
- Save as pandas DataFrames in a dictionary. 

#### `002-process-data`
- Filter gene counts for top 5000 most variable genes and top 10 most prevelant tissues excluding sparse genes. 
- Log normalize and standardize to mean 0 and sd of 1. 

#### `003-reduced-dims`
- Calculate 50 principal components on gene counts matrix.

#### `004-cluster`
- Try multiple parameters for HDBSCAN clustering and choose the optimal one based on silhouette, adjusted rand score, and normalized mutual information. 
- Do the same with GMM but mostly using BIC
- Look at how cluster overlaps with tissue type

#### `005-characterize-clusters`
- Run Wilcoxon-Sum-Rank test on each cluster's ith gene expression _g_ versus every other cluster's pooled _g_
- Do the same between tissues
- Reference literature to see how tissue expression lines up