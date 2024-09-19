import pandas as pd
import glob
import os
import sqlite3
from collections import Counter

#Query all receiving data from both tables by the Wide Receiver position
con = sqlite3.connect("raw_data/receiving_data.db")
cur = con.cursor()

nflWR = pd.read_sql_query("SELECT * from NFL where position == 'WR'", con)
ncaaWR = pd.read_sql_query("SELECT * from NCAA where position == 'WR'", con)

con.close() 

#drop all columns that are not player and player_id
merged = pd.merge(ncaaWR, nflWR, left_on=['player','player_id'], right_on=['player','player_id'], how='inner')
columns_drop = list((Counter(list(merged.columns))-Counter(['player','player_id'])).elements())
merged.drop(columns=columns_drop, inplace=True)

#get the list of WRs who are in both the NCAA and NFL datasets
player_list = merged.drop_duplicates()

#Create separate dfs with WR players who have played in the NCCA and the NFL
ncaa = ncaaWR[ncaaWR['player_id'].isin(player_list['player_id'])]
nfl = nflWR[nflWR['player_id'].isin(player_list['player_id'])]

ncaa = ncaa.reset_index(drop=True)
nfl = nfl.reset_index(drop=True)

unique_ncaa = ncaa.drop_duplicates('player_id')

#Keep features we will use for classification in both DFs
cols_keep = ['year', 'player', 'player_id','player_game_count', 'avg_depth_of_target', 'avoided_tackles','caught_percent','drops','grades_hands_drop',
       'grades_hands_fumble', 'grades_offense','grades_pass_route','route_rate', 'routes', 'slot_rate', 'slot_snaps',
       'targeted_qb_rating', 'targets', 'touchdowns', 'wide_rate','wide_snaps','routes','receptions', 'yards', 'yards_after_catch','yards_after_catch_per_reception', 'yards_per_reception', 'yprr']

nfl_filter = nfl[cols_keep]
ncaa_filter = ncaa[cols_keep]

#Groupby player_id in both DFs
groupby_NFL = nfl_filter.groupby('player_id')
groupby_ncaa = ncaa_filter.groupby('player_id')

#Replace all Nans with column means
final_season = groupby_ncaa.tail(1)
nan_cols = list(final_season.columns[final_season.isnull().any(axis=0)])
nanDF = final_season.loc[:,nan_cols].copy(deep=False)

for i in nan_cols:     #---Applying Only on variables with NaN values
    nanDF.loc[:,i].fillna(nanDF.loc[:,i].mean(), inplace=True)
    final_season[i] = nanDF[i]
    
final_season.isnull().values.any()

#reset index
final_season = final_season.reset_index(drop=True)

#Create y-label DF
players = final_season[['player','player_id']]
players = pd.concat([players,pd.DataFrame(columns=list(('800_yard_season','1000_yard_season')))])
players.player_id = players.player_id.astype(int)

for idx,row in players.iterrows():
    
    player_id = row['player_id']
    player_history = nfl.loc[nfl['player_id'] == player_id]
    
    for idx, row in player_history.iterrows():
        if row['yards'] > 800:
            players.loc[players['player_id'] == player_id,'800_yard_season'] = 1
            
        if row['yards'] > 1000:
            players.loc[players['player_id'] == player_id,'1000_yard_season'] = 1
            
    if pd.isna(players.loc[players['player_id'] == player_id,'800_yard_season'].item()):
        players.loc[players['player_id'] == player_id,'800_yard_season'] = 0
        
    if pd.isna(players.loc[players['player_id'] == player_id,'1000_yard_season'].item()):
        players.loc[players['player_id'] == player_id,'1000_yard_season'] = 0

data = final_season
labels = players

data.to_csv('final_data/data.csv', index=False)
labels.to_csv('final_data/labels.csv', index=False)