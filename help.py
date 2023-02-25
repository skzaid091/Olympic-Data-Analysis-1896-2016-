def medal_tally(df):

    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally


def country_year_list(df):

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')

    years = sorted(df['Year'].unique().tolist())
    years.insert(0, 'Overall')

    return country, years


def country_year_result(df, country_d, year_d):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if (country_d == 'Overall') and (year_d == 'Overall'):
        temp_df = medal_df
    if (country_d != 'Overall') and (year_d == 'Overall'):
        flag = 1
        temp_df = medal_df[medal_df['region'] == country_d]
    if (country_d == 'Overall') and (year_d != 'Overall'):
        temp_df = medal_df[medal_df['Year'] == year_d]
    if (country_d != 'Overall') and (year_d != 'Overall'):
        temp_df = medal_df[(medal_df['region'] == country_d) & (medal_df['Year'] == year_d)]

    if flag == 1:
        temp_df = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()
        temp_df['Year'] = temp_df['Year'].astype(str)
    else:
        temp_df = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    temp_df['Total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']

    return temp_df


def data_over_time(df, col):

    n_data_over_time = df.drop_duplicates([col, 'Year'])['Year'].value_counts().reset_index().sort_values('index')

    n_data_over_time.rename(columns={'index': 'Year', 'Year': col}, inplace=True)

    return n_data_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals', 'Sport': 'Sport', 'region': 'Country'}, inplace=True)

    return x


def year_wise_medal_tally(df, country):

    country_wise_tally = df.dropna(subset=['Medal'])
    country_wise_tally.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    temp = country_wise_tally[country_wise_tally['region'] == country]
    n_temp = temp.groupby('Year').count()['Medal'].reset_index()

    return n_temp


def country_sports_wise(df, country):
    dd = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp = dd[dd['region'] == country]
    return temp


def most_successful_athletes_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def age_plot(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    return x1, x2, x3, x4


def age_plot_sport_wise(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    sport_df = athlete_df[athlete_df['Sport'] == sport]
    sport_df = sport_df[sport_df['Medal'] == 'Gold']['Age'].dropna()
    sport_df = sport_df.reset_index()['Age']
    sport_df = sport_df.tolist()
    return sport_df


def height_weight_df(df, country, sport):
    temp_df = df.drop_duplicates(subset=['Name', 'region'])
    temp_df['Medal'].fillna('No Medal', inplace=True)
    title = ''
    if (country == 'Overall') and (sport == 'Overall'):
        temp = temp_df
        title = 'Overall Height vs Weight Distribution'
    if (country != 'Overall') and (sport == 'Overall'):
        temp = temp_df[temp_df['region'] == country]
        title = 'Overall Height vs Weight Distribution of ' + country
    if (country == 'Overall') and (sport != 'Overall'):
        temp = temp_df[(temp_df['Sport'] == sport)]
        title = 'Overall Height vs Weight Distribution in ' + sport
    if (country != 'Overall') and (sport != 'Overall'):
        temp = temp_df[(temp_df['region'] == country) & (temp_df['Sport'] == sport)]
        title = 'Overall Height vs Weight Distribution of ' + country + ' in ' + sport
    return temp, title
