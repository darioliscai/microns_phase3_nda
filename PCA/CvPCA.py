from typing import Literal
from sklearn.decomposition import PCA
import numpy as np

class CvPCA(PCA):
    
    def __init__(self) -> None:
        super().__init__()
    
    def fit_cv(self, X_train: np.array, X_test:np.array) -> np.array:
        self.fit(X_train)
        train_components = self.components_
        C = X_train.shape[0]
        cv_singular_values = np.linalg.multi_dot([train_components.T, X_test.T, X_train, train_components]) / C 
        return cv_singular_values
    
def cvPCA(X):
    ''' X is 2 x stimuli x neurons '''
    pca = PCA(n_components=min(1024, X.shape[1])).fit(X[0].T)
    u = pca.components_.T
    sv = pca.singular_values_
    
    xproj = X[0].T @ (u / sv)
    cproj0 = X[0] @ xproj
    cproj1 = X[1] @ xproj
    ss = (cproj0 * cproj1).sum(axis=0)
    return ss