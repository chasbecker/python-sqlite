# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 11:49:45 2020

@author: Charles
"""
print("Welcome to GitHell")

import pandas as pd
import sqlite3 as s3

# it is better to use DB Browser to load data directly to the db
# this is provided as a round trip example
#
# Read the csv file, write it as a table to an existing sqlite3 db
##################################################################
imp_df = pd.read_csv(r".\data\city_temperature.csv",
                     dtype={'Region':object,
                            'Country':object,
                            'State':object,
                            'City':object,
                            'Month':int,
                            'Day': int,
                            'Year':int,
                            'AvgTemperature':float})

# gotcha!  python renders excessive precision
imp_df.round({'AvgTemperature':1})

con = s3.connect(r".\data\city_temperature.db")
imp_df.to_sql( "ct", con, if_exists='replace', index=False )

con.close()


                                                            
# query the db
#
# tn = table name
# cs = column(s) string
# ws = 'where' string
##################################################################

tn = 'ct'
cs = "*"
ws = "Year=2012 AND Month=7"

con = s3.connect(r".\data\city_temperature.db")
a_df = pd.read_sql_query("SELECT " + cs + "FROM " + tn + " WHERE " + ws, con)

# write query result to table
##################################################################
a_df.to_sql( "2012temp", con, if_exists="replace", index=False )

con.close()

# read the query data from db to a dataframe
##################################################################
con = s3.connect(r".\data\city_temperature.db")
b_df = pd.read_sql( "SELECT * FROM '2012temp'", con )
con.close()