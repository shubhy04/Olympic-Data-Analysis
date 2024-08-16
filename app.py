import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import preprocessor,helper
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.markdown("<h1 style='font-size: 36px; font-weight: bold; color:#FFD700;'>Olympic Analysis</h1>", unsafe_allow_html=True)

st.sidebar.image("D:\\DA_Project\\Olympics-Web-app\\logo.png")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

# Medal Tally
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select an Option", years)
    selected_country = st.sidebar.selectbox("Select an Option", country)
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Tally")
    if selected_year == "Overall" and selected_country != "Overall":
        st.title(selected_country + " Overall Performance")
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year != "Overall" and selected_country != "Overall":
        st.title(selected_country+ " Performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)

# Overall Analysis
if user_menu == "Overall Analysis":
    # no of editions
    editions = df['Year'].unique().shape[0] - 1  # 1906 not considered
    # no of Hosts
    cities = df['City'].unique().shape[0]
    # no of sports
    sports = df['Sport'].unique().shape[0]
    # no of events
    events = df['Event'].unique().shape[0]
    # no of athletes
    athletes = df['Name'].unique().shape[0]
    # participating nation
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    # Line charts
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Editions', y='region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Editions', y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Editions', y='Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    # Heat map - It shows that over the years the events occurred in each sports
    st.title("No. of events over the time(Every year)")
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year' , values = 'Event', aggfunc = 'count').fillna(0).astype(int),annot=True)

    # Set the figure and axes background to transparent
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Set the color of x-ticks and y-ticks to white
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Set the color of the x and y labels for better visibility
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    # Set the color of the tick labels for better visibility
    plt.setp(ax.get_xticklabels(), color='white')
    plt.setp(ax.get_yticklabels(), color='white')

    st.pyplot(fig)

    # Most Successful Athletes
    st.title('Most Successful Athletes')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    selected_sport = st.selectbox("Select a Sport", sports_list)
    msa = helper.most_successful(df,selected_sport)
    st.table(msa)

# Country-wise Analysis
if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select a country", country_list)

    # Line Chart
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    # Heat Map
    st.title(selected_country + " excels in following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot = True)
    st.pyplot(fig)

    # Top 10 Successful athletes
    st.title(selected_country + " Top 10 Athletes")
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

# Athlete wise Analysis
if user_menu == 'Athlete wise Analysis':

    # Line CHart that show in which age the probability of winning gold,silver,bronze is high
    st.title("Distribution of Age")
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()     # It shows the age distribution of all the athletes
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x3], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize = False , width = 1000 , height = 600)
    st.plotly_chart(fig)

    # Line Chart that shows the probability of winning gold medal for a particular sport in the particular age
    st.title("Distribution of Age wrt to Sports(Gold Medalist)")
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    # Scatter Plot that shows Particular sport height vs weight comparison
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    selected_sport = st.selectbox("Select a Sport", sports_list)
    temp_df = helper.weight_vs_height(df,selected_sport)
    fig,ax = plt.subplots()

    medal_palette = {
        'Gold': 'gold',
        'Silver': 'silver',
        'Bronze': '#cd7f32',
        'No Medal': 'blue'
    }
    ax = sns.scatterplot(x =temp_df['Weight'],y =temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60, palette=medal_palette)
    st.title(f'Weight vs. Height for {selected_sport} Athletes')
    st.pyplot(fig)

    # Line chart that shows Male Vs Female Participation Over the Years
    final = helper.men_vs_women(df)
    st.title("Male Vs Female Participation Over the Years")
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

