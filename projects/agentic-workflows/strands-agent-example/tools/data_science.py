from strands import tool
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.inspection import permutation_importance
from sklearn.utils.fixes import parse_version
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

# @tool
# def get_data():
#     return load_breast_cancer()
methods = [
    load_breast_cancer, 
    RandomForestClassifier,
    AdaBoostClassifier,
    BaggingClassifier,
    permutation_importance,
    parse_version,
    train_test_split
    ]
ds_tools = [tool(method) for method in methods]