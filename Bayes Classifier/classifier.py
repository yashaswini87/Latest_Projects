from collections import defaultdict
import numpy as np
from pandas import DataFrame, Series

class NaiveBayes(object):
    """
    Represents naive bayes classifier. Instances are constructed with training
    data and options to configure the classifier.

    Parameters
    ----------
    training_data: sequence of tuples as [(label, [features])]
      e.g., [("good", ["hello", "world"])]
    log: boolean, default False
      Whether to transform the computed probabilities into log space
    smoothing: float, default 0.
      Amount of additive smoothing
    """
    def __init__(self, training_data, log=False, smoothing=0.):
        """
        Parameters
        ----------
        training_data: sequence of tuples as [(label, [features])]
          e.g., [("good", ["hello", "world"])]
        log: boolean, default False
          Whether to transform the computed probabilities into log space
        smoothing: float, default 0.
          Amount of additive smoothing
        """
        # Assign variables to unique ids
        self.log = log 
        self.smoothing = smoothing 
        self.train(training_data) 

    def train(self, data):
        """
        Re-train the classifier with given input training data.
        The effects of previous training are overridden

        Parameters
        ----------
        data: sequence of tuples as [(label, [features])]
          e.g., [("positive", ["hello", "world"])]
          
        """
        self._curr_data = data
        if data is not None:
	    ## calling train_data function to find the label(prior) distribution and conditional distribution
            self._label_dist, self._cond_dist = train_data(data,self.smoothing) 
	    ## finding the labels in label_counts dictionary. For eg: if _label_dist is {good:3, bad:2}, then _label_dist_sample= {good,bad} 	         ## grabs labels. "samples" is misleading.
	    self._labels = self._label_dist.samples

    def classify(self, data, prob=False):
        """
        Classify a given set of features, optionally return the estimated
        probability

        Parameters
        ----------
        data: sequence of str [features]
          e.g., ["hello", "world"]
        prob: boolean, default False
          Whether to return the estimated probability as well
        """

	# Null case. Return nothing.
        if data is None or len(data) == 0:
            if prob:
                return None, np.nan
            else:
                return None
	
        post = Series(self._calc_post(data)) ## Calculating the posterior 
        max_label = post.idxmax() # Grab most probable label
        if not prob:
            return max_label # Return most probable label
        return max_label, post[max_label] # Return label and probability of label

    def _calc_post(self, data):
        """
        Parameters
        ----------
        data: list or ndarray
        prob: bool, default True
          Also return probabilities if true
        """
        data = self._discard_missing(data) # Not a misnomer. Discards incomplete data pairs
        label_priors = self._calc_label_priors() # Grabs prior prob of each label
        post_raw = self._handle_conditional(label_priors, data) # Returns unnormalized posterior prob
        post = self._normalize(post_raw) # Normalizes posterior prob (i.e. sum of probs = 1)
        return post

    def _discard_missing(self, data):
        clean_data = []
        # HEY! Also has a SIDE EFFECT (!!!!---!.)
        for feature in data: # Searches for (label,feature) pairs and adds them to data
            for label in self._labels:
                if (label, feature) in self._cond_dist:
                    clean_data.append(feature)
                    break # This may have unintended consequences!!! Will only grab first pair...

        return clean_data

    @property
    def _prob_fname(self):
        return 'logprob' if self.log else 'prob' # Use this to determine whether to calc logp or p later...

    @property
    def agg(self):
        import operator as op
        return op.add if self.log else op.mul # Just creates a + or * operator for big Sigma and big Pi notation

    @property
    def _label_pfunc(self):
        return getattr(self._label_dist, self._prob_fname) # _label_dist._prob_fname, where _prof_fname = prob or logprob

    def _get_cond_pfunc(self, label, feature):
        pdist = self._cond_dist[(label, feature)]
        return getattr(pdist, self._prob_fname) # pdist._prob_fname, where _prob_fname = prob or logprob

    # separate function in case we need to tweak this
    ## This function calculates prior
    def _calc_label_priors(self):
        return self._label_pfunc()
    
    # First step toward calculating conditional probs
    def _handle_conditional(self, priors, data):
        post = priors.copy()
        [self._label_cond_helper(label, data, post) for label in self._labels] # Don't use list... just a for-loop to generate product of conditional probs
        return post 
    
    def _label_cond_helper(self, label, data, prob):
        # ! SIDE EFFECT
        for feature in data:
            value = True # BoW
            pfunc = self._get_cond_pfunc(label, feature) # Grabs associated cond. prob from dictionary
            prob[label] = self.agg(prob[label], pfunc(value)) # Running product of cond. probs
            
    # Normalizes conditional probs such that their sum is 1
    def _normalize(self, post):
        if self.log: # For log-scaled prob
            value_sum = np.log(post).sum()
            if not np.isfinite(value_sum):
                post[:] = np.log(1.0 / len(post)) # If log(0), weight all equally
            else:
                post -= value_sum # Else subtract sum (which is like division...)
        else:
            value_sum = post.sum()
            if value_sum == 0:
                post[:] = 1.0 / len(post) # If probs = 0, weight equally
            else:
                post /= value_sum # Else, divide by sum of probs
        return post

class ProbDist(object):

    # NOTE: value_counts = label_counts... confusing, since value = True/False elsewhere
    def __init__(self, value_counts, smooth=0.):
        self._value_counts = Series(value_counts) ## Convert into pandas series  
        self._N = self._value_counts.sum()## summing value_counts 
        self._bins = len(self._value_counts) ## counting the value_counts
        self._smooth = 0.5 

    @property
    def total(self):
        return self._N + self._bins * self._smooth # 'smoothed' total number of 'articles'

    # NOTE: samples = list of labels... not sure why it's called samples
    @property
    def samples(self):
        return self._value_counts.index # returns the labels from label_counts

    def prob(self, feature=None):
        """
        Parameters
        ----------
        feature: object, optional
          If None or unspecified then returns prob for all distinct samples
        """
        
        # NOTE: Below feature can = label. Confusing since elsewhere feature = word
        p = (self._value_counts.get(feature, 0) 
             if feature else self._value_counts) # Grab count. Let count = 0 if there is no count.
        return (p + self._smooth) / self.total # Return smoothed frequency = p... estimate of prob

    def logprob(self, feature=None):
        """
        Parameters
        ----------
        feature: object, optional
          If None or unspecified then returns log prob for all distinct samples
        """
        # NOTE: Below feature can = label. Confusing since elsewhere feature = word
        p = (self._value_counts.get(feature, 0) 
             if feature else self._value_counts) # Grab count. Let count = 0 if there is no count.
        return (np.log(p + self._smooth) - np.log(self.total))# Return smoothed frequency = p... estimate of prob


def train_data(data, smoothing=0.):
    """
    Parameters
    ----------
    data: nested dict
    """
    ## Directs to gather freq counts
    (label_counts, feature_values,
    conditional, conditional_count) = _gather_freq_counts(data)

    # side-effect!
    ## Missing features tags False to label & feature combo which has occured less than the ncounts(which is the number of times a label occurs in 	the data) 
    ## It takes input form _gather_freq_counts	
    _fill_missing_features(label_counts, feature_values,
                           conditional, conditional_count)
    ## Calls ProbDist class which takes input as a dictionary with label and its occurence in data to calculate the prior
    label_prior = ProbDist(label_counts, smoothing)
    cond_dist = {(label, feature) : ProbDist(fcounts, smoothing)
                 for ((label, feature), fcounts)
                 in conditional.iteritems()}

    return label_prior, cond_dist

def _gather_freq_counts(data):
    """
    computes:
    1. num occurrences by label
    2. set of distinct values by feature
    3. num samples per value by label/feature
    4. num samples per label/feature
    """
    label_counts = defaultdict(int)
    feature_values = defaultdict(set)
    conditional = defaultdict(lambda: defaultdict(int))
    conditional_count = defaultdict(int)

    for label, featureset in data:
        label_counts[label] += 1 # Counts number of good/bad documents
        for feature in featureset:
            value = True # BoW
            conditional[(label, feature)][value] += 1 # Increment observation of coincident label and feature
            conditional_count[(label, feature)] += 1 # Increment 
            feature_values[feature].add(value)

    return (label_counts, feature_values,
            conditional, conditional_count)

def _fill_missing_features(label_counts, feature_values,
                           conditional, conditional_count):
    """
    Compute features that do NOT occur for a label

    Notes
    -----
    Has side effect
    """
    for label, nsamples in label_counts.iteritems():
        for feature in feature_values.iterkeys():
            count = conditional_count[(label, feature)]
            conditional[(label, feature)][False] = nsamples - count
            feature_values[feature].add(False)
