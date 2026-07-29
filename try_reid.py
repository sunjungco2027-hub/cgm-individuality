"""quick try: can a nearest-neighbor tell whose meal it is?"""
import sys
sys.path.insert(0, "src")

from sklearn.neighbors import KNeighborsClassifier

import fingerprint as fp

Z, subjects = fp.residual_matrix()
knn = KNeighborsClassifier(n_neighbors=10, metric="cosine").fit(Z, subjects)
print("resubstitution acc:", (knn.predict(Z) == subjects).mean())
