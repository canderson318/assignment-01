
# /Users/canderson/miniconda3/envs/cu-cpbs-7602/bin/python /Users/canderson/Documents/school/CPBS7602-class/assignment-01/version001/src/002-process-data.py
import pandas as pd
import numpy as np  
import os 
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

os.chdir("/Users/canderson/Documents/school/CPBS7602-class/assignment-01/version001")

with open("processed-data/001-dat-dict.pkl",'rb') as f:
    dat_dict = pickle.load(f)

type(dat_dict)
len(dat_dict)
dat_dict.keys()
for key, value in dat_dict.items():
    print(f"{key}: {value.shape}")

with open("processed-data/001-dat-dict.pkl",'rb') as f:
    dat_dict = pickle.load(f)

type(dat_dict)
len(dat_dict)
dat_dict.keys()
for key, value in dat_dict.items():
    print(f"{key}: {value.shape}")

# Create a working subset:
### From metadata: select the top 10 tissues with the largest sample size.
### From the gene expression file: select the top 5,000 most variable genes.
### Be mindful of memory usage when using .var() — consider efficient .read_csv usage.
### If needed, reduce sample or gene count (using the same logic).
### Generate a unified dataset with:
###     Inputs: samples from top tissues, represented by genes
###     Targets: tissue labels
### Standardize the input data.

for col in dat_dict["colData"]:
    print(col)
    print(dat_dict["colData"][col].unique()[:10])

#\\\
#\\\
# Select top 10 count tissues
#\\\
#\\\
# Frequency table for the 'SMTS' column
tiss_freqs=dat_dict["colData"]['SMTS'].value_counts(dropna=False, sort = True)
print(tiss_freqs)

top_tiss=tiss_freqs.index[0:10]

# bool of top_tiss obs
tiss_inds = dat_dict["colData"]['SMTS'].isin(top_tiss).values

# filter data_dict for these obs
def filter_se(SE, margin=None, indices=None):
    if margin == 0:
        # filter genes (rows)
        return {
            "counts": SE['counts'].iloc[indices, :],
            "rowData": SE['rowData'].iloc[indices, :],
            "colData": SE['colData']  # unchanged
        }

    elif margin == 1:
        # filter samples (columns)
        return {
            "counts": SE['counts'].iloc[:, indices],
            "rowData": SE['rowData'],  # unchanged
            "colData": SE['colData'].iloc[indices, :]
        }

    else:
        raise ValueError("margin must be 0 (rows/genes) or 1 (columns/samples)")

dat_dict = filter_se(dat_dict, 1, tiss_inds)

# check if correct 
sum(tiss_inds)==dat_dict["counts"].shape[1]

#\\\
#\\\
# Select top 5000 most variable genes
#\\\
#\\\

# first exclude missy genes
## gene missing proportions
zero_sum = (dat_dict['counts']==0).sum(axis=1).values
zero_prop = zero_sum / (dat_dict['counts'].shape[1])
pd.Series(zero_prop).describe()

x, bins = np.histogram(zero_prop)

# plt.figure()
# plt.hist(bins[:-1],weights =  x)
# plt.show()

# select for genes with < 60% 0s
non_missy_genes = zero_prop<.6
dat_dict = filter_se(dat_dict, margin = 0, indices = non_missy_genes)

# Compute variance for each gene 
variance = dat_dict["counts"].var(axis=1)

x, y = range(len(variance.values)), sorted(np.log1p(variance))

top_y = y[-5000:]
len(top_y)
is_top = np.zeros(len(y), dtype = bool)
is_top[-5000:]= True

# plt.figure()
# p1 = plt.scatter(
#     x, y, c=is_top, s=10, cmap=plt.cm.Paired
# )
# plt.xlabel("Ind")
# plt.ylabel("Variance")
# plt.show()

# select top genes
dat_dict = filter_se(dat_dict, 0, is_top)

# \\\
# \\\
# Standardize data
# \\\
# \\\

# plot gene distributions
# from scipy.stats import gaussian_kde

# def plot_density(x, add=False, color=None, label=None, show=True):
#     x = np.asarray(x)

#     # KDE density
#     kde = gaussian_kde(x)
#     xs = np.linspace(x.min(), x.max(), 500)
#     ys = kde(xs)

#     # If add=False, start a new figure
#     if not add:
#         plt.figure()

#     plt.plot(xs, ys, color=color, label=label)

#     if label is not None:
#         plt.legend()

#     plt.xlabel("x")
#     plt.ylabel("Density")
#     plt.title("Density estimate (Gaussian KDE)")

#     # Show plot only if not adding more lines
#     if show and not add:
#         plt.show()

# # # First density: create a new figure via add=False
# # plot_density(dat_dict['counts'].iloc[0, :].values, add=False, color="C0", show=False)

# # # Add more densities on top
# # for rw in range(3):
# #     print(rw)
# #     x = dat_dict['counts'].iloc[rw, :].values
# #     plot_density(x, add=True, color=f"C{rw+1}", show=False)

# # plt.show()

# lognormalize
## colSums
libsize = dat_dict['counts'].sum(axis=0) # sum across rows= colsums
# sum normalize columns and multiply by scaling factor so each sample sum is same
norm = dat_dict['counts'].div(libsize, axis=1) * 10_000
# log normalize
lognorm = np.log1p(norm)

# standardize 
## gene rowmeans
mean = lognorm.mean(axis=1) # axis 1 = across columns
## rowSds
std = lognorm.std(axis=1,  ddof=1)   
## centered and scaled
Z = lognorm.sub(mean, axis=0).div(std, axis=0)

dat_dict["logcounts"]= Z


# # First density: create a new figure via add=False
# plot_density(dat_dict['logcounts'].iloc[0, :].values, add=False, color="C0", show=False)

# # Add more densities on top
# for rw in range(3):
#     print(rw)
#     x = dat_dict['logcounts'].iloc[rw, :].values
#     plot_density(x, add=True, color=f"C{rw+1}", show=False)

# plt.show()

with(open("processed-data/002-dat-dict.pkl", 'wb') as f ):
    pickle.dump(dat_dict, f)

print("Done")

