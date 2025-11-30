# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-execution,-papermill,-trusted
#     notebook_metadata_filter: -jupytext.text_representation.jupytext_version
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# /Users/canderson/miniconda3/envs/cu-cpbs-7602/bin/python /Users/canderson/Documents/school/CPBS7602-class/assignment-01/src/py/005*.py
import pandas as pd
import numpy as np  
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import pickle

# %%
os.chdir("/Users/canderson/Documents/school/CPBS7602-class/assignment-01")


# %%
# load data
dat_dict = pickle.load( open("processed-data/004-dat-dict.pkl", 'rb') )

# %% [markdown]
# ### Genes Driving Clustering

# %% [markdown]
# #### wilcoxon sum rank test for each cluster versus every other
#

# %%
# Transpose to sample x gene
adata = sc.AnnData((dat_dict['counts']+ 1e-9).T)

# %%
# Add clusters to metadata
adata.obs["cluster"] = pd.Categorical(dat_dict['colData'].gmm_clusters.values)

# %%
# Add Tissue to metadata
adata.obs["tissue"] = pd.Categorical(dat_dict['colData'].SMTS.values)


# %%
# extract results from test
def cluster_results(adata, var, group):
    """Extract DE results for a single group."""
    res = adata.uns["rank_genes_groups"]
    g = str(group)

    return pd.DataFrame({
        "gene":  res["names"][g],
        "logFC": res["logfoldchanges"][g],
        "pval":  res["pvals"][g],
        "padj":  res["pvals_adj"][g],
        "score": res["scores"][g],
        var:      group
    })


# %%
# run test on scanpy object 
def get_markers(adata, var):
    """Run DE for a variable and return combined markers for all groups."""
    
    sc.tl.rank_genes_groups(adata, groupby=var, method="wilcoxon")
    
    groups = adata.obs[var].unique().tolist()
    
    dfs = []
    for g in groups:
        df = cluster_results(adata, var, g)
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


# %%
tissue_markers = get_markers(adata, "tissue").merge(dat_dict['rowData'], 
                                left_on  = "gene", 
                                right_on = "Name")
cluster_markers = get_markers(adata, "cluster").merge(dat_dict['rowData'], 
                                left_on  = "gene", 
                                right_on = "Name")


# %% [markdown]
# ##### filter for top genes for each grouping

# %%
tissue_tops = (
    tissue_markers
    .assign(abs_score = tissue_markers['score'].abs())
    .sort_values(['abs_score'], ascending=[False])
    .groupby('tissue')
    .head(1)
)


# %%
cluster_tops = (
    cluster_markers
    .assign(abs_score = cluster_markers['score'].abs())
    .sort_values(['abs_score'], ascending=[False])
    .groupby('cluster')
    .head(1)
)

# %%
cluster_tops

# %%
tissue_tops

# %% [markdown]
# ### Results
# Above I printed the top most characteristic genes per cluster and tissue type. I cross referenced the tissue results with genecards and my results capture the gene expression documentation. 
#
# For example, ELAVL3 is asscociated with brain tissue and this is confirmed by other studies ([link](https://www.genecards.org/cgi-bin/carddisp.pl?gene=ELAVL3&keywords=ELAVL3))

# %% [markdown]
#
