import numpy as np
import pandas as pd


def modified_zscore(data, consistency_correction):
    """
    Returns the modified z score and Median Absolute Deviation (MAD) from the scores in data.
    The consistency_correction factor converts the MAD to the standard deviation for a given
    distribution. A value of 1.4826 is used if the underlying data
    is normally distributed

    Parameters:
        data : input data
        consistency_correction : Adjustment to relate median to standard deviation
    Returns:
        mod_zscore : modified z score
    """
    median = np.median(data)
    deviation_from_med = np.array(data) - median
    mad = np.median(np.abs(deviation_from_med))
    mod_zscore = deviation_from_med / (consistency_correction * mad)
    return mod_zscore

def extract_outliers(list_in,consistency_correction,threshold):
    """
    Returns the modified z score and Median Absolute Deviation (MAD) from the scores in data.
    The consistency_correction factor converts the MAD to the standard deviation for a given
    distribution. A value of 1.4826 is used if the underlying data
    is normally distributed
    Parameters:
        list_in : list of data to identify outliers in
        consistency_correction : Adjustment to relate median to standard deviation
        threshold : the cutoff for outlier identification
    Returns:
        outlier_prices : prices that are outliers based on the threshold
    """
    if len(list_in) >=3:
        # list_in = list_in[1:]
        mod_zs = modified_zscore(list_in, consistency_correction)
        res = [idx for idx, val in enumerate(mod_zs) if (val > threshold) or (val < -1.0*threshold)]
        if len(res) > 1:
            outlier_prices = [list_in[i] for i in tuple(res)]
        else:
            outlier_prices = [None]
    else:
        outlier_prices = [None]
    return outlier_prices


# Creating sample data
data = {
    'propertytype': ['MF', 'OF', 'RT', 'LO', 'IN', 'MF', 'OF', 'RT', 'LO', 'IN'],
    'comps_prices_persize': [
        [100, 102, 98, 97, 105, 250],  # MF (outlier at 250)
        [200, 202, 205, 199, 210, 1000],  # OF (outlier at 1000)
        [50, 55, 53, 52, 51, 300],  # RT (outlier at 300)
        [500, 505, 510, 495, 10000],  # LO (outlier at 10000)
        [30, 32, 31, 30, 400],  # IN (outlier at 400)
        [110, 115, 112, 111, 109],  # MF (no outliers)
        [190, 195, 192, 200, 198],  # OF (no outliers)
        [45, 50, 48, 49, 47],  # RT (no outliers)
        [490, 495, 500, 505, 510],  # LO (no outliers)
        [28, 30, 29, 27, 26]  # IN (no outliers)
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

threshold = 2.5
consistency_correction=1.4826
ptypes = ['MF','OF','RT','LO','IN']
for ptype in ptypes:
    print(f"Processing property type : {ptype}")
    df_prop = df[df['propertytype'] == ptype].copy().reset_index(drop=True)
    df_prop['price_persize_outliers'] = df_prop.apply(lambda x: extract_outliers(x['comps_prices_persize'],consistency_correction,threshold), axis=1)
print()