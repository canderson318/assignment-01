# /Users/canderson/miniconda3/envs/cu-cpbs-7602/bin/python /Users/canderson/Documents/school/CPBS7602-class/assignment-01/version001/src/003-reduced-dims.py
import pandas as pd
import numpy as np  
import os 
import pickle
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns

os.chdir("/Users/canderson/Documents/school/CPBS7602-class/assignment-01/version001")

with open("processed-data/002-dat-dict.pkl",'rb') as f:
    dat_dict = pickle.load(f)


#\\\
#\\\
# impute NAs
#\\\
#\\\

na_sum = dat_dict['logcounts'].isna().sum(axis=1).values
na_prop = na_sum / (dat_dict['logcounts'].shape[1])

counts, bins = np.histogram(na_prop)
# plt.figure()
# plt.hist(bins[:-1], bins, weights=counts)
# plt.show()

# \\\
# \\\
# calculate reduced dimensions
# \\\
# \\\

# fit PCA to capture 95% of variance (change n_components as needed)
pcs_file = "processed-data/pcs.pkl"
print("Running PCA…")
pca = PCA(n_components=50, svd_solver='auto', random_state=0)
scores = pca.fit_transform(np.transpose(dat_dict['logcounts']))
scores = np.transpose(scores)
print("PCA finished")

scores.shape
pca.explained_variance_ratio_.sum()

df = pd.DataFrame(np.transpose(scores)).iloc[:, :2].copy()
df["var"] = dat_dict["colData"]["SEX"].values

# sns.pairplot(df,
#              hue="var",
#              plot_kws={'s': 10})
# plt.show()
# plt.close()

# add to dat_dict
dat_dict['rDims']= {"PCA": {"scores": scores, "attributes": pca}}


#\\\
#\\\
# Save
#\\\
#\\\

with(open("processed-data/003-dat-dict.pkl", 'wb') as f ):
    pickle.dump(dat_dict, f)

print("Done")
