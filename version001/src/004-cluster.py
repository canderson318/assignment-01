
# /Users/canderson/miniconda3/envs/cu-cpbs-7602/bin/python /Users/canderson/Documents/school/CPBS7602-class/assignment-01/version001/src/004-reduced-dims.py
import pandas as pd
import numpy as np  
import os 
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import HDBSCAN
from sklearn.metrics import silhouette_score
from sklearn.metrics import adjusted_rand_score

os.chdir("/Users/canderson/Documents/school/CPBS7602-class/assignment-01/version001")


# load data
dat_dict = pickle.load( open("processed-data/003-dat-dict.pkl", 'rb') )


# # plot pcs by tissue
# plot_df = pd.DataFrame(np.transpose(dat_dict["rDims"]["PCA"]["scores"])).iloc[:, :2]
# plot_df['Tissue']= dat_dict["colData"]['SMTS']
# sns.pairplot(
#     plot_df, 
#     hue = 'Tissue', 
#     plot_kws = {'s': 1}
# )

#\\\\
#\\\\
# cluster using hdbscan
#\\\\
#\\\\

def print_keys(d, indent=0):
    if isinstance(d, dict):
        for key in d.keys():
            print("  " * indent + str(key))
            print_keys(d[key], indent + 1)

print_keys(dat_dict)

clusterer = HDBSCAN(min_cluster_size=30)
cluster_labels = clusterer.fit_predict(np.transpose(dat_dict['rDims']['PCA']['scores']))


# Build the plotting dataframe
plot_df = pd.DataFrame(np.transpose(dat_dict["rDims"]["PCA"]["scores"][:2, :]), 
                       columns=["PC1", "PC2"])
plot_df["cluster"] = pd.Series(cluster_labels)

plt.scatter(
    plot_df["PC1"],
    plot_df["PC2"],
    c=plot_df["cluster"],
    cmap="tab20",   
    s=3,
    alpha=0.7
)


res = []
X = dat_dict['rDims']['PCA']['scores'].T
true_labels = dat_dict['colData']['SMTS']

for i in range(10, 150, 5):
    clusterer = HDBSCAN(min_cluster_size=i)
    cluster_labels = clusterer.fit_predict(X)
    sl = silhouette_score(X, cluster_labels)
    ars = adjusted_rand_score(true_labels, cluster_labels)
    res.append({"num": i, "ARS": ars, "SL": sl})

res = pd.DataFrame(res)
print(res)

sns.pairplot(res)

res.num[np.argmax(res.ARS)]
res.num[np.argmax(res.SL)]

# \\\
# \\\
# save data
# \\\
# \\\

pth = "processed-data/004-dat-dict.pkl"
print(f"Saving {pth}")
pickle.dump(dat_dict, open(pth, "wb"))
print("Done")