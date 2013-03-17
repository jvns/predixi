import os
import pandas as pd
from datetime import datetime

def date_converter(x):
    """
    Helper function to deal with some issues in the input CSVs
    """
    if len(str(x)) == 0:
        return 0
    else:
        return datetime.fromtimestamp(int(x) / 1000)

def read_data(datadir):
    """
    Read all data from CSVs in data directory and concatenate together
    """
    days = []
    for filename in sorted(os.listdir(datadir)):
        try:
            day = pd.read_csv(datadir + filename, index_col=['id', 'latestUpdateTime'], converters={'latestUpdateTime': date_converter})
            day = day.drop_duplicates().dropna(axis=1, how='all')
            days.append(day)
        except:
            print "Failed to parse", filename
    return pd.concat(days)

def generate_features(series):
    import random
    from datetime import timedelta
    ts = series['nbBikes'].resample('2min', fill_method='ffill', how='mean')
    timestamps = random.sample(ts.index, 1000)
    transformed = pd.DataFrame(index=timestamps, columns=['actual', '5min', '30min', '60min', '2hr'], dtype='float64')
    for time in timestamps:
        transformed.set_value(time, 'actual', float(ts.ix[time]))
        try:
            transformed.set_value(time, '5min', ts.ix[time - timedelta(minutes=6)])
            transformed.set_value(time, '30min', ts.ix[time - timedelta(minutes=30)])
            transformed.set_value(time, '60min', ts.ix[time - timedelta(minutes=60)])
            transformed.set_value(time, '2hr', ts.ix[time - timedelta(hours=2)])
        except:
            pass
    return transformed.dropna()
