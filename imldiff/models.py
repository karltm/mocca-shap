from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
import numpy as np


class SteppedLogisticRegression(LogisticRegression):
    
    def decision_function(self, X):
        scores = super(SteppedLogisticRegression, self).decision_function(X)
        return scores.astype(int).astype(float)

    
class RuleClassifier(BaseEstimator, ClassifierMixin):
    
    def  __init__(self, decision_rule):
         self.decision_rule = decision_rule

    def fit(self, X, y):
        X, y = check_X_y(X, y) 
        self.classes_ = unique_labels(y)
        return self

    def predict(self, X):
        check_is_fitted(self)
        X = check_array(X)
        result = np.apply_along_axis(self.decision_rule, 1, X)
        y = np.take(self.classes_, result.astype(int))
        return y


