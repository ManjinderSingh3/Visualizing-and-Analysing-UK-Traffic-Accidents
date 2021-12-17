from typing import Dict

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN

def dbscan(df: pd.DataFrame, eps) -> Dict:
    minimum_samples = 25
    model = DBSCAN(eps=eps, min_samples = minimum_samples, metric='euclidean')
    clusters = model.fit_predict(df)
    labels = model.labels_
    unique_labels = np.unique(model.labels_)

    return dict(model=model, clusters=labels, unique_clusters=unique_labels)

