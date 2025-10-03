import agents.data_science as ds_agent

if __name__ == "__main__":
    #ds_agent.agent("Load breast cancer data.")
    
    # Adapted from https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance_multicollinear.html
    prompt = """
    In this example, we compute the permutation_importance of the features to a trained RandomForestClassifier 
    using the Breast cancer Wisconsin (diagnostic) dataset. The model can easily get about 97% accuracy on a test dataset. 
    Because this dataset contains multicollinear features, the permutation importance shows that none of the features are important, 
    in contradiction with the high test accuracy.
    
    Demo a possible approach to handling multicollinearity, which consists of hierarchical clustering on the features’ 
    Spearman rank-order correlations, picking a threshold, and keeping a single feature from each cluster.
    
    For the purposes of this demo you can just use a small subset of the data. 
    """
    ds_agent.agent(prompt=prompt)