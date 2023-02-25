import pandas as pd


def processor(df, region_df):

    df = df[df['Season'] == 'Summer']

    data = df.merge(region_df, on='NOC', how='left')

    data.drop_duplicates(inplace=True)

    data = pd.concat([data, pd.get_dummies(data['Medal'])], axis=1)

    return data
