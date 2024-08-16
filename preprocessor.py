import pandas as pd


def preprocess(df, region_df):

    # filtering summer data
    df = df[df['Season'] == 'Summer']

    # merging region dataset
    df = df.merge(region_df, on='NOC', how='left')

    # dropping duplicated
    df.drop_duplicates(inplace=True)

    dummies = pd.get_dummies(df['Medal']).astype(int)

    df = pd.concat([df, dummies], axis=1)

    return df
