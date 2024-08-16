import numpy as np

def fetch_medal_tally(df,years,country):
    medal_df= df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if years == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if years == 'Overall' and country != 'Overall':
        flag =1
        temp_df = medal_df[medal_df['region'] == country]
    if years != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(years)]
    if years != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == 2016) & (medal_df['region'] == 'India')]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def medal_tally(df):

    # dropping duplicates to solve the medal value for each team player
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    country = np.unique(df['region'].dropna()).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def data_over_time(df,col):
    over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    over_time.rename(columns={'Year': 'Editions', 'count': col }, inplace=True)
    return over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset = ['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x= temp_df['Name'].value_counts().reset_index().merge(df, on = 'Name' , how = 'left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns = {'count':'Medals'},inplace = True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.drop_duplicates(subset='Medal')
    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year')['Medal'].count().reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.drop_duplicates(subset='Medal')
    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year' , values = 'Medal', aggfunc = 'count').fillna(0)
    return pt

def most_successful_countrywise(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x= temp_df['Name'].value_counts().reset_index().head(15).merge(df, on = 'Name' , how = 'left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns = {'count':'Medals'},inplace = True)
    return x

def weight_vs_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left').fillna(0).astype(int)
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final