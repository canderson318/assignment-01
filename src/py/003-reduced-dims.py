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
# /Users/canderson/miniconda3/envs/cu-cpbs-7602/bin/python /Users/canderson/Documents/school/CPBS7602-class/assignment-01/src/py/003-reduced-dims.py
import pandas as pd
import numpy as np  
import os 
import pickle
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns

# %%
os.chdir("/Users/canderson/Documents/school/CPBS7602-class/assignment-01")

# %%
with open("processed-data/002-dat-dict.pkl",'rb') as f:
    dat_dict = pickle.load(f)


# %% [markdown]
# ### Remove sparse genes 

# %%
na_sum = dat_dict['logcounts'].isna().sum(axis=1).values
na_prop = na_sum / (dat_dict['logcounts'].shape[1])
print(na_prop)
# ^^ not necessary

# %% [markdown]
# ### Calculate reduced dimensions

# %%
# fit PCA to capture 95% of variance (change n_components as needed)
print("Running PCA…")
pca = PCA(n_components=50, svd_solver='auto', random_state=0)
scores = pca.fit_transform(np.transpose(dat_dict['logcounts']))
scores = np.transpose(scores)
print("PCA finished")

# %%
scores.shape
pca.explained_variance_ratio_.sum()

# %%
df = pd.DataFrame(np.transpose(scores)).iloc[:, :2].copy()
df["tissue"] = dat_dict["colData"]["SMTS"].values
sns.pairplot(df,
             hue="tissue",
             plot_kws={'s': 10})
plt.show()
plt.close()

# %%
# add to dat_dict
dat_dict['rDims']= {"PCA": {"scores": scores, "attributes": pca}}


# %% [markdown]
# ### Save

# %%
print("Saving...")
with(open("processed-data/003-dat-dict.pkl", 'wb') as f ):
    pickle.dump(dat_dict, f)
print("Done")
