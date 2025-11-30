# /Users/canderson/miniconda3/envs/cu-cpbs-7602/bin/python /Users/canderson/Documents/school/CPBS7602-class/assignment-01/version001/src/003-reduced-dims.py
import pandas as pd
import numpy as np  
import os 
import pickle
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.stats import gaussian_kde

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
plt.figure()
plt.hist(bins[:-1], bins, weights=counts)
# plt.show()

# \\\
# \\\
# calculate reduced dimensions
# \\\
# \\\

# fit PCA to capture 95% of variance (change n_components as needed)
pca = PCA(n_components=0.80, svd_solver='auto', random_state=0)
scores = pca.fit_transform(dat_dict['logcounts'])
 
