from scipy import stats
import numpy as np
from statsmodels.robust.scale import mad

def remove_outliers(data, test, n_sd=5, n_medmad=3.5, method='zdist'):
    """
    Remove outliers from a distribution

    Arguments
    ---------
    data: numpy array
        continuous values with possible outliers
    n_sd: int, default 3
        the number of standard deviations to use as cut-off for zdist
    n_medmad: float, default 3.5
        the value above which data are outliers for medmad
    method: str, options ['zdist', 'medmad'], default zdist
        method to use for identifying outliers. Medmad may be more robust
        to extreme skew but unsure.
    """
    if method == 'zdist':
        outliers = np.where(np.abs(stats.zscore(data.loc[:, test])) < n_sd, True, False)
    elif method == 'medmad':
        outliers = med_mad(data.loc[:, test].values, cut_point=n_medmad)
    else:
        raise ValueError('Method type not supported')
    data = data.loc[outliers, :]

    return data


def med_mad(x, cut_point = 3.5, cut_off=True):
    medmad = np.abs((x - np.median(x)) / mad(x))

    if cut_off:
        return medmad < cut_point
    else:
        return medmad


def transform_variable(var, transform_choice):
    if transform_choice == 1:
        if any(var < 0): 
            return np.log(var + (np.abs(np.min(var)) + 1)) 
        elif 0 in var:
            return np.log1p(var)
        else:
            return np.log(var)
    elif transform_choice == 2:
        if any(var < 0): 
            return np.sqrt(var + np.abs(np.min(var)))
        else:
            return np.sqrt(var)
    elif transform_choice == 3:
        x, _ = stats.yeojohnson(var)
        return x
    else:
        raise ValueError('Transform option not supported')


def rescale_data(data, clip_range, test, z_transform):
     if clip_range != 0:
         assert clip_range in [1, 2]
         if clip_range == 1:
            data = remove_outliers(data, test, method='zdist')
         elif clip_range == 2:
            data = remove_outliers(data, test, method='medmad')
         else:
             raise ValueError('Outlier removal not supported')
     if len(z_transform) == 1:
         assert z_transform[0] == 0
         data.loc[:, test] = ((data.loc[:, test] - data.loc[:, test].mean()) /
                              data.loc[:, test].std())
     
     return data
