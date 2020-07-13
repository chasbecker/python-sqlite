# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 11:38:57 2020

The function 'GetSelect' takes four params:
    con: a connection
    tn: a table name
    cs: either a list of columnn names to return or '*' for all columns 
    ws: a "where string" being the parameters that define the WHERE clause
    
It returns a dataframe with column names.

Dataset was downloaded from: https://www.kaggle.com/sudalairajkumar/daily-temperature-of-major-cities
as a csv file.  Using DB Browser: https://sqlitebrowser.org/ I imported the csv file into an sqlite
database ("city_temperature.db").  So that's how that happened, and it happened very quickly.

@author: Charles (Chuck) Becker (c.l.becker@outlook.com)

"""
# import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 as s3
import seaborn as sns
import time

def GetSelect( con, cs, tn, ws ):
    cur = con.cursor()
    query_string = "SELECT " + cs + " FROM " + tn + " WHERE " + ws
    
    # get a list of column names for the dataframe
    if cs == '*':
        cnlist = []    
        cur.execute( "PRAGMA table_info(" + tn + ")" )
        cnq = cur.fetchall()
        for entry in cnq:
            cnlist.append( entry[1] )
    else:
        cslist = cs.split(',')
        cnlist = [c.strip() for c in cslist]

    cur.execute( query_string )
    rezult = pd.DataFrame( cur.fetchall() )
    rezult.columns = cnlist
        
    return rezult


#
# set parameters here
##################################
con1 = s3.connect( r".\data\city_temperature.db")
columns_string = "City, Month, Year, AvgTemperature" # or e.g; for column subset
table_name = "ct"
where_string = "AvgTemperature > 75 AND AvgTemperature < 85"


########function call#############
tic = time.perf_counter()
a_df = GetSelect( con1, columns_string, table_name, where_string )
toc = time.perf_counter()
print( "TimeToExecute: " + str( toc - tic ))

sns.distplot( a_df['AvgTemperature'], rug = True )

print("All done")