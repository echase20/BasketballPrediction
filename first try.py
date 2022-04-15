import pandas as pd

from pandas.core.dtypes.common import is_integer_dtype

pd.set_option('display.max_columns', None)
url = 'https://www.basketball-reference.com/players/t/tatumja01/gamelog/2022'
df = pd.read_html(url, header = 0)
df = df[7]
df = df.drop(df[df.Age == 'Age'].index)

df.drop(df.columns[0], axis=1, inplace=True)
df.drop(df.columns[4], axis=1, inplace=True)
df.drop(df.columns[6], axis=1, inplace=True)
df = df[df['FG'] != 'Inactive']
df = df.reset_index()
df.drop(labels=['index'], axis=1, inplace=True)
#print(df.head())

url2 = 'https://www.basketball-reference.com/players/t/tatumja01/splits/'
df_team = pd.read_html(url2, header = 0)
df_team = df_team[0]
df_team = df_team.iloc[53:84]
df_team.columns = df_team.iloc[0]
df_team.drop(labels=53, axis=0, inplace=True)
df_team = df_team.reset_index()
df_team = df_team.iloc[:, [2, 31]]
#print(df_team)

#print(df)

#for i in range(df.shape[0]):
    #print(df.loc[i][1])

df_names = pd.read_csv('NBAteamnames - Sheet1.csv')
df_names = df_names.astype({'Opp': 'string'})
#print(df_names)
#print(df_names.dtypes)
df_date_abb = df.loc[:, ['Date', 'Opp']]
df_date_abb = df_date_abb.astype({'Opp': 'string'})
#print(df_date_abb)
#print(df_date_abb.dtypes)
joined = df_date_abb.merge(df_names, on='Opp')
joined.sort_values(by='Date', axis=0, inplace=True)
joined = joined.reset_index()
joined.drop(labels=['index'], axis=1, inplace=True)
#print(joined)
opp_list = []
date = joined.loc[0][0]
url3 = 'https://www.teamrankings.com/nba/stat/opponent-points-per-game?date={}'.format(date)
opp_ppg_df = pd.read_html(url3, header = 0)
opp_ppg_df = opp_ppg_df[0]
snippet = opp_ppg_df.loc[opp_ppg_df['Team'] == joined.loc[0][3]]
snippet = snippet.reset_index()
opp_list.append(snippet.loc[0][8])
#print(joined)
for i in range(joined.shape[0] - 1):
    date=joined.loc[i+1][0]
    url3 = 'https://www.teamrankings.com/nba/stat/opponent-points-per-game?date={}'.format(date)
    opp_ppg_df = pd.read_html(url3, header = 0)
    opp_ppg_df = opp_ppg_df[0]
    team = joined.loc[i+1][3]
    if joined.loc[i+1][3] == 'Oklahoma City':
        team = 'Okla City'
    if joined.loc[i+1][3] == 'New Jersey':
        team = 'Brooklyn'
    snippet = opp_ppg_df.loc[opp_ppg_df['Team'] == team]
    snippet = snippet.reset_index()
    opp_list.append(snippet.loc[0][3])
df['Opp_ppg'] = opp_list
print(df)