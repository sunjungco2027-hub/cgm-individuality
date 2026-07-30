"""quick look at the within vs between distance spread."""
import sys
sys.path.insert(0, "src")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_distances

import fingerprint as fp

Z, s = fp.residual_matrix()
D = cosine_distances(Z)
iu = np.triu_indices(len(s), k=1)
same = (s[:, None] == s[None, :])[iu]

plt.hist(D[iu][same], bins=40, alpha=0.6, label="within")
plt.hist(D[iu][~same], bins=40, alpha=0.6, label="between")
plt.legend()
plt.savefig("hist.png")
print("saved hist.png")
