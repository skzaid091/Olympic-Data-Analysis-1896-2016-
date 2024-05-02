import streamlit as st
import pandas as pd
# import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import preprocessor, help

st.set_page_config(layout='wide')


def empty_space():
    col4, col5, col6 = st.columns(3)
    with col4:
        st.write('')
        st.write('')
        st.write('')
    with col5:
        pass
    with col6:
        pass


data1 = pd.read_excel('data/athlete_events_1.xlsx')
data1.drop('Unnamed: 0', axis=1, inplace=True)
data2 = pd.read_excel('data/athlete_events_2.xlsx')
data2.drop('Unnamed: 0', axis=1, inplace=True)

events_data = pd.concat([data1, data2], axis=1, join='inner')
regions_data = pd.read_csv('data/noc_regions.csv')

df = preprocessor.processor(events_data, regions_data)

st.sidebar.title('Olympics Analysis')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Country-Wise Analysis', 'Overall Analysis', 'Athlete-Wise Analysis')
)

country_data, year_data = help.country_year_list(df)
sport_df = df['Sport'].unique().tolist()

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    country = st.sidebar.selectbox('Select Country', country_data)
    year = st.sidebar.selectbox('Select Year', year_data)

    medal_tally = help.country_year_result(df, country, year)
    if country == 'Overall' and year == 'Overall':
        st.title('Overall Tally')
    if country == 'Overall' and year != 'Overall':
        st.title('Medal Tally in ' + str(year) + ' Olympics')
    if country != 'Overall' and year == 'Overall':
        st.title(country + ' Overall Performance')
    if country != 'Overall' and year != 'Overall':
        st.title(country + ' Performance in ' + str(year))
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    Editions = df['Year'].unique().shape[0] - 1
    Cities = df['City'].unique().shape[0]
    Sports = df['Sport'].unique().shape[0]
    Events = df['Event'].unique().shape[0]
    Athletes = df['Name'].unique().shape[0]
    Nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    empty_space()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.subheader(Editions)
    with col2:
        st.header("Cities")
        st.subheader(Cities)
    with col3:
        st.header("Sports")
        st.subheader(Sports)

    empty_space()

    col7, col8, col9 = st.columns(3)
    with col7:
        st.header("Events")
        st.subheader(Events)
    with col8:
        st.header("Athletes")
        st.subheader(Athletes)
    with col9:
        st.header("Nations")
        st.subheader(Nations)

    empty_space()
    empty_space()

    st.title('Participating Nations over Time')
    nations_over_time = help.data_over_time(df, 'region')


    empty_space()

    # st.title('Number of Events over Time')
    # number_of_events_o_time = help.data_over_time(df, 'Event')
    # fig_events = px.line(number_of_events_o_time, x='Year', y='Event')
    # st.plotly_chart(fig_events)

    # empty_space()

    # st.title('Number of Athletes over Time')
    # number_of_events_o_time = help.data_over_time(df, 'Name')
    # fig_events = px.line(number_of_events_o_time, x='Year', y='Name')
    # st.plotly_chart(fig_events)

    # empty_space()

    st.title('No. of Events over Time')
    fig, ax = plt.subplots(figsize=(15, 15))
    y = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(y.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.plotly_chart(fig)

    empty_space()


    sport_df.sort()
    sport_df.insert(0, 'Overall')
    sport = st.sidebar.selectbox('Select Sport', sport_df)

    if sport == 'Overall':
        st.title('Most Successful Athletes')
    if sport != 'Overall':
        st.title('Most Successful Athletes in ' + str(sport))

    quality_data = help.most_successful(df, sport)
    st.table(quality_data)

if user_menu == 'Country-Wise Analysis':
    # nations = df['region'].dropna().unique().tolist()

    # country_t = st.sidebar.selectbox('Select Country', nations)

    # country_Graph = help.year_wise_medal_tally(df, country_t)

    # fig = px.line(country_Graph, x="Year", y="Medal")
    # st.title(country_t + ' Medal Tally over the Years')
    # st.plotly_chart(fig)

    # empty_space()

    x = help.country_sports_wise(df, country_t)
    fig2, ma = plt.subplots(figsize=(15, 15))
    ma = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int), annot=True)
    st.title(country_t + ' Medals in each Sport over the Years')
    st.plotly_chart(fig2)

    empty_space()

    successful_athletes = help.most_successful_athletes_country_wise(df, country_t)
    successful_athletes = successful_athletes.iloc[0:10]
    st.title(country_t + '\'s 10 Most Successful Athletes')
    st.table(successful_athletes)

if user_menu == 'Athlete-Wise Analysis':

    x1, x2, x3, x4 = help.age_plot(df)
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             colors=['Blue', 'Yellow', 'Brown', 'Green'], show_rug=False, show_hist=False)

    st.title('Age Plot of Athletes')
    st.plotly_chart(fig)

    empty_space()

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing',
                     'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
                     'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis',
                     'Golf', 'Softball', 'Archery', 'Vollyball', 'Synchronized Swimming', 'Table Tennis',
                     'Baseball' 'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Vollyball', 'Triathlon', 'Rugby', 'Polo',
                     'Ice Hockey']

    sport = st.sidebar.selectbox('Select Sport for Age Plot of Athletes', famous_sports)

    x = help.age_plot_sport_wise(df, sport)
    fig3 = ff.create_distplot([x], [sport], colors=['Blue'], show_rug=False, show_hist=False)
    st.title('Distribution of Age for ' + sport + ' (Gold Medalist)')
    st.plotly_chart(fig3)

    empty_space()

    st.sidebar.text('          ')
    st.sidebar.subheader('Height and Weight Distribution')
    country1 = st.sidebar.selectbox('Select Country', country_data)
    sport_df.insert(0, 'Overall')
    sport1 = st.sidebar.selectbox('Select Sport', sport_df)

    temp, title = help.height_weight_df(df, country1, sport1)
    st.title(title)
    fig3, fx = plt.subplots()
    fx = sns.scatterplot(data=temp, x='Weight', y='Height', style='Sex', hue='Medal', s=40)
    plt.figure(figsize=(10, 10))
    st.plotly_chart(fig3)


