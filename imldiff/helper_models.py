from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
import numpy as np


round_with_precision = lambda X, precision: precision * np.round((1/precision) * X)


class ModifiedClassifier(BaseEstimator, ClassifierMixin):

    def  __init__(self, base_model):
        check_is_fitted(base_model)
        self.base_model = base_model
        self.classes_ = base_model.classes_
        self.predict = lambda X: self._postprocess_labels(
            self.base_model.predict(self._preprocess(X)), X)

        if hasattr(self.base_model, 'predict_proba'):
            self.predict_proba = lambda X: self._postprocess_proba(
                self.base_model.predict_proba(self._preprocess(X)), X)

        if hasattr(self.base_model, 'predict_log_proba'):
            self.predict_log_proba = lambda X: self._postprocess_log_proba(
                self.base_model.predict_log_proba(self._preprocess(X)), X)

    def fit(self, X, y):
        return self

    def _preprocess(self, X):
        return X

    def _postprocess_labels(self, y, X):
        return y

    def _postprocess_proba(self, y, X):
        return y

    def _postprocess_log_proba(self, y, X):
        return y


class SteppedLogisticRegression(LogisticRegression):
    
    def decision_function(self, X):
        scores = super(SteppedLogisticRegression, self).decision_function(X)
        return scores.astype(int).astype(float)

    
# TODO: refactor usages of rule classifier
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
        return self.decision_rule(X)


class LogProbabilityMixin:
    
    def predict_log_proba(self, X):
        return np.log(self.predict_proba(X))
