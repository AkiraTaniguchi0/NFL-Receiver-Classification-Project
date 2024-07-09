import pandas as pd
import glob
import os
import sqlite3
from collections import Counter

#Get all the data file names  in the data folder
path = r'data' 
all_files = glob.glob(path + "/*.csv")

#Create a dictionary where every key is the name of the csv file and the value that corresponds is the csv file converted to a pandas dataframe.
#https://stackoverflow.com/questions/56949605/how-to-read-each-file-from-a-folder-and-create-seperate-data-frames-for-each-fil
d = {os.path.splitext(os.path.basename(f))[0] : pd.read_csv(f) for f in all_files} 

#create a list of tuples where each tuple is (name of csv,dataframe)
#https://stackoverflow.com/questions/10795973/python-dictionary-search-values-for-keys-using-regular-expression
ncaa_list = [(key, value) for key, value in d.items() if key.startswith("ncaa_")]

#add year column to each dataframe
for entry in ncaa_list:
    if 'year' not in entry[1].columns:
        name = entry[0][len(entry[0]) - 2:]
        year = "20"+name
        entry[1].insert(0, 'year', int(year))

#concat dfs in list into one df
ncaa_all = pd.DataFrame()
for i in ncaa_list:
    ncaa_all = pd.concat([ncaa_all,i[1]])

#do the above for NFL data
nfl_list = [(key, value) for key, value in d.items() if key.startswith("nfl_")]

for entry in nfl_list:
    if 'year' not in entry[1].columns:
        name = entry[0][len(entry[0]) - 2:]
        year = "20"+name
        entry[1].insert(0, 'year', int(year))

nfl_all = pd.DataFrame()
for i in nfl_list:
    nfl_all = pd.concat([nfl_all,i[1]])



def create_sqlite_database(filename):
    """ create a database connection to an SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(filename)
        print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_sqlite_database("data/receiving_data.db")

conn = sqlite3.connect('data/receiving_data.db')

nfl_all.to_sql('NFL', conn, if_exists='fail')
ncaa_all.to_sql('NCAA', conn, if_exists='fail')
conn.close()

