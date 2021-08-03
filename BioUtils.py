import numpy

def sklearn_metrics_roc_curve(y_true, y_score, direct=True, pos_label=None):
    """Calculate true and false positives per binary classification threshold.

    Parameters
    ----------
    y_true : ndarray of shape (n_samples,)
        True targets of binary classification.

    y_score : ndarray of shape (n_samples,)
        Estimated probabilities or output of a decision function.

    pos_label : int or str, default=None
        The label of the positive class.

    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.

    Returns
    -------
    fps : ndarray of shape (n_thresholds,)
        A count of false positives, at index i being the number of negative
        samples assigned a score >= thresholds[i]. The total number of
        negative samples is equal to fps[-1] (thus true negatives are given by
        fps[-1] - fps).

    tps : ndarray of shape (n_thresholds,)
        An increasing count of true positives, at index i being the number
        of positive samples assigned a score >= thresholds[i]. The total
        number of positive samples is equal to tps[-1] (thus false negatives
        are given by tps[-1] - tps).

    thresholds : ndarray of shape (n_thresholds,)
        Decreasing score values.
    """

    # make y_true a boolean vector
    if y_true.dtype != bool:
        y_true = (y_true == pos_label)

    # sort scores and corresponding truth values
    if direct:
        desc_score_indices = numpy.argsort(y_score, kind="mergesort")[::-1]
    else:
        desc_score_indices = numpy.argsort(-y_score, kind="mergesort")[::-1]
    y_score = y_score[desc_score_indices]
    y_true = y_true[desc_score_indices]

    # y_score typically has many tied values. Here we extract
    # the indices associated with the distinct values. We also
    # concatenate a value for the end of the curve.
    distinct_value_indices = numpy.where(numpy.diff(y_score))[0]
    threshold_idxs = numpy.r_[distinct_value_indices, y_true.size - 1]

    # accumulate the true positives with decreasing threshold
    tps = numpy.cumsum(y_true)[threshold_idxs]
    fps = 1 + threshold_idxs - tps
    thresholds = y_score[threshold_idxs]

    # Attempt to drop thresholds corresponding to points in between and
    # collinear with other points. These are always suboptimal and do not
    # appear on a plotted ROC curve (and thus do not affect the AUC).
    # Here np.diff(_, 2) is used as a "second derivative" to tell if there
    # is a corner at the point. Both fps and tps must be tested to handle
    # thresholds with multiple data points (which are combined in
    # _binary_clf_curve). This keeps all cases where the point should be kept,
    # but does not drop more complicated cases like fps = [1, 3, 7],
    # tps = [1, 2, 4]; there is no harm in keeping too many thresholds.
    optimal_idxs = numpy.where(numpy.r_[True, numpy.logical_or(numpy.diff(fps, 2), numpy.diff(tps, 2)), True])[0]
    fps = fps[optimal_idxs]
    tps = tps[optimal_idxs]
    thresholds = thresholds[optimal_idxs]

    # Add an extra threshold position
    # to make sure that the curve starts at (0, 0)
    if direct:
        if pos_label is not None:
            tps = numpy.r_[0, tps]
            fps = numpy.r_[0, fps]
            thresholds = numpy.r_[pos_label, thresholds]
    else:
        tps = numpy.r_[0, tps]
        fps = numpy.r_[0, fps]
        thresholds = numpy.r_[0, thresholds]

    fpr = fps / fps[-1]
    tpr = tps / tps[-1]

    return fpr, tpr, thresholds
