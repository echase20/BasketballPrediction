import pandas as pd
def team_stats(first_name, last_name): #gets the stats of the current player vs. every other team
    initial = last_name[0]
    first_initials = first_name[0:2]
    link_name = last_name + first_initials
    url2 = 'https://www.basketball-reference.com/players/{}/{}01/splits/'.format(initial, link_name)
    df_team = pd.read_html(url2, header=0)
    df_team = df_team[0] # selects the correct df
    df_team = df_team.iloc[53:84] #gets the rows we need
    df_team.columns = df_team.iloc[0] # selects the column headers
    df_team.drop(labels=53, axis=0, inplace=True) # drops the column headers from the first row
    df_team = df_team.reset_index() # resets the index
    df_team = df_team.iloc[:, [2, 31]] # selects team name column and pts average column
    return df_team


def get_stats(first_name, last_name): #goes to the current years game log for the given player and reads to a df
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    #This section reads the players game long for the current year to a dataframe and does clean up
    initial = last_name[0]
    first_initials = first_name[0:2]
    link_name = last_name + first_initials
    url = 'https://www.basketball-reference.com/players/{}/{}01/gamelog/2022'.format(initial,link_name)
    df = pd.read_html(url, header=0)
    df = df[7] # selects the correct df
    df = df.drop(df[df.Age == 'Age'].index) # drops duplicate headers
    #df.drop(df.columns[0], axis=1, inplace=True)
    #df.drop(df.columns[4], axis=1, inplace=True)
    #df.drop(df.columns[6], axis=1, inplace=True) #drops rows that are not needed
    df.drop(df.columns[[0,3, 5,7, 8,9,11,13,14,16,17,19,20,25,26,28,29]], axis=1, inplace=True)
    df = df[df['FG'] != 'Inactive'] # drops games which they did not play in
    df = df[df['FG'] != 'Did Not Dress']
    df = df[df['FG'] != 'Not With Team']
    df = df.reset_index() #resets the index number
    df.drop(labels=['index'], axis=1, inplace=True) #drops the new index column


    #This section grabs a df of nba teams, names, and abbreviations and merges it with the players
    # oppenents and dates this season
    df_names = pd.read_csv('NBAteamnames - Sheet1.csv')
    df_names = df_names.astype({'Opp': 'string'})
    # print(df_names.dtypes)
    df_date_abb = df.loc[:, ['Date', 'Opp']]
    df_date_abb = df_date_abb.astype({'Opp': 'string'})
    # print(df_date_abb)
    # print(df_date_abb.dtypes)
    joined = df_date_abb.merge(df_names, on='Opp')
    joined.sort_values(by='Date', axis=0, inplace=True)
    joined = joined.reset_index()
    joined.drop(labels=['index'], axis=1, inplace=True)
    #print(joined)

    # This section takes that merged df and loops through the dates to find the opponents ppg for every matchup.
    # it then takes that list of averages and adds it to our game long df.
    opp_list = []
    date = joined.loc[0][0]
    url3 = 'https://www.teamrankings.com/nba/stat/opponent-points-per-game?date={}'.format(date)
    opp_ppg_df = pd.read_html(url3, header=0)
    opp_ppg_df = opp_ppg_df[0]
    snippet = opp_ppg_df.loc[opp_ppg_df['Team'] == joined.loc[0][3]]
    snippet = snippet.reset_index()
    opp_list.append(snippet.loc[0][8])
    # print(joined)
    for i in range(joined.shape[0] - 1):
        date = joined.loc[i + 1][0]
        url3 = 'https://www.teamrankings.com/nba/stat/opponent-points-per-game?date={}'.format(date)
        opp_ppg_df = pd.read_html(url3, header=0)
        opp_ppg_df = opp_ppg_df[0]
        team = joined.loc[i + 1][3]
        if joined.loc[i + 1][3] == 'Oklahoma City':
            team = 'Okla City'
        if joined.loc[i + 1][3] == 'New Jersey':
            team = 'Brooklyn'
        snippet = opp_ppg_df.loc[opp_ppg_df['Team'] == team]
        snippet = snippet.reset_index()
        opp_list.append(snippet.loc[0][3])
    df['Opp_ppg'] = opp_list
    #print(df)

    # This sections takes the players averages against every team in the league and joines it with the game
    # log table so we have that players points average against the opponent for every game
    df_team = team_stats(first_name, last_name)
    #print(df_team)
    team_ppg_against = joined.merge(df_team, left_on='City', right_on='Value')
    team_ppg_against.sort_values(by='Date', axis=0, inplace=True)
    team_ppg_against.rename(columns={'PTS': 'ppg_against_team'}, inplace=True)
    df = df.merge(team_ppg_against, on='Date')
    df.drop(df.columns[[14,15,17]], axis=1, inplace=True)
    df.rename(columns={'Opp_x': 'Opp'}, inplace=True)

    # This section will calculate the players ppg avg throughout the season and make a new column for it
    ppg_list = []
    ppg_list.append(str(get_career_avg(first_name, last_name)))
    ppg_list.append(df.loc[0][12])

    for i in range(joined.shape[0] - 2):
        last_game = df.loc[i+1][12]
        pt_total = float(ppg_list[-1])*(i+1)
        avg_so_far = (float(last_game) + pt_total)/(i+2)
        ppg_list.append(str(avg_so_far))
    df['avg_ppg'] = ppg_list
    print(df)


def get_career_avg(first_name, last_name):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    initial = last_name[0]
    first_initials = first_name[0:2]
    link_name = last_name + first_initials
    url = 'https://www.espn.com/nba/player/_/id/4065648/{}-{}'.format(first_name, last_name)
    df = pd.read_html(url, header=0)
    df = df[2]
    return df.loc[1][11]

get_stats('Jayson','Tatum')
print(get_career_avg('Jayson', 'Tatum'))