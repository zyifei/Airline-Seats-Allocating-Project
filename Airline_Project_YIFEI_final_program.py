
# coding: utf-8

# # Airline Project

# #### Import library 

# In[27]:

import sqlite3
import pandas as pd
import numpy as np


# #### Define functions

# In[28]:

def update_metrics_table(refused, separated):
    c.execute("UPDATE metrics SET passengers_refused = ? , passengers_separated = ? ;",(refused,separated))
    conn.commit() # this is a Python command

def small_than_max(aircraft_left_number, people_in_group, booking_name):
    best_row_index = find_the_best_row(aircraft_left_number, people_in_group)
    fit_into_aircraft(people_in_group,best_row_index, booking_name)
    
def fit_into_aircraft(people_in_group,best_row_index, booking_name):
    i = 0 
    left_seats = aircraft_left_number.iloc[best_row_index]["left_seats_number"] 
    left_index = aircraft_left_index.iloc[best_row_index]["left_seats_Index"]
    while(i < people_in_group):
        new_index = left_index + i
        if aircraft.iloc[best_row_index][new_index] == 0:
            aircraft.iloc[best_row_index][new_index] = 1
            #update to the database, since the sircraft changed
            row = best_row_index + 1
            seat = seat_letter[new_index]
            update_seating_table(booking_name, row, seat)
            
        i += 1
    aircraft_left_number.iloc[best_row_index]["left_seats_number"] = left_seats - people_in_group
    aircraft_left_index.iloc[best_row_index]["left_seats_Index"] = left_index + people_in_group

    
    
def update_seating_table(booking_name, row, seat):
    query = ("UPDATE seating SET name = '%s' WHERE  row = %d AND seat = '%s';" % (booking_name, row, seat))
    c.execute(query)
    conn.commit()

    
#this function is used for find the best number of seat to fit in all people in the booking group
#return the best row index
#the next function should be update aircraft 
def find_the_best_row(aircraft_left_number, people_in_group):
    numpyMatrix = aircraft_left_number["left_seats_number"].as_matrix()
    best_row_index = find_nearest_above(numpyMatrix, people_in_group)

    return best_row_index
    
def find_nearest_above(my_array, target):
    diff = my_array - target
    mask = np.ma.less(diff, 0)
    # We need to mask the negative differences and zero
    # since we are looking for values above
    if np.all(mask):
        return None # returns None if target is greater than any value
    masked_diff = np.ma.masked_array(diff, mask)
    return masked_diff.argmin()

    
def split_into_two_group(people_in_group):
    if(people_in_group%2 == 1):
        people_in_group_1 = (people_in_group - 1)/2
        people_in_group_2 = (people_in_group + 1)/2
        same = 0
    else:
        people_in_group_1 = people_in_group_2 = people_in_group/2
        same = 1
    return same, people_in_group_1, people_in_group_2


# new one:
def bigger_than_max(aircraft_left_number,people_in_group, split_number):
    result = split_number
    left_max = aircraft_left_number["left_seats_number"].max()
    if left_max == 0 :
        return result
        
    same, people_in_group_1, people_in_group_2 = split_into_two_group(people_in_group)
    if people_in_group_1 == 1:
        split_number += 1
        result = split_number
    if people_in_group_2 == 1:
        split_number += 1
        result = split_number
    #same = 1
    if same == 1:
        if (people_in_group_1 > left_max) & (people_in_group_2 > left_max) :
            split_number = bigger_than_max(aircraft_left_number,people_in_group_1, split_number)
            split_number = bigger_than_max(aircraft_left_number,people_in_group_2, split_number)
        else:
            small_than_max(aircraft_left_number, people_in_group_1, booking_name)
            if people_in_group_2 <= aircraft_left_number["left_seats_number"].max(): 
                small_than_max(aircraft_left_number, people_in_group_2, booking_name)
            else:
                split_number += bigger_than_max(aircraft_left_number,people_in_group_2, split_number)
    else:
        if (people_in_group_1 > left_max) & (people_in_group_2 > left_max) :
            split_number = bigger_than_max(aircraft_left_number,people_in_group_1, split_number)
            split_number = bigger_than_max(aircraft_left_number,people_in_group_2, split_number)
        else:
            if (people_in_group_1 <= left_max) & (people_in_group_2 <= left_max) :
                small_than_max(aircraft_left_number, people_in_group_2, booking_name)
                if people_in_group_1 <= aircraft_left_number["left_seats_number"].max():
                    small_than_max(aircraft_left_number, people_in_group_1, booking_name)
                else: 
                    split_number = bigger_than_max(aircraft_left_number,people_in_group_1, split_number)
            else:
                small_than_max(aircraft_left_number, people_in_group_1, booking_name)
                split_number = bigger_than_max(aircraft_left_number,people_in_group_2, split_number)
    result = split_number
    return result


def get_total_refused_passagers(index_i):
    i = index_i + 1
    refused_number = 0
    while(i < total_bookings_number):
        refused_number += bookings.iloc[i][1].tolist()
        i += 1
    return refused_number
  
    
# the lengh of the rows = len(index)

def aircraft_left_number_index(aircraft_df, rows_number,seats_located):
    i = 0    
    while(i < rows_number):
        occupied_number = 0
        if(aircraft_df.iloc[i]['name'] != ''):
            occupied_number += 1
            j = i + rows_number # the index for the same row with different seats
            while(j  < len(aircraft_df)):
                if(aircraft_df.iloc[j]['name'] != ''):
                    occupied_number += 1
                j += rows_number
            aircraft_left_number.iloc[i]["left_seats_number"] = len(columns) - occupied_number
            aircraft_left_index.iloc[i]["left_seats_Index"] = occupied_number
            seats_occupied = 0
            while(seats_occupied < occupied_number): 
                aircraft.iloc[i][seats_occupied] = 1
                seats_occupied += 1
            seats_located += occupied_number
        i += 1 
        
    return aircraft, aircraft_left_number, aircraft_left_index, seats_located


# #### Import Database and Bookings.csv

# ##### Database

# In[29]:


conn = sqlite3.connect('data.db') # create a "connection"

c = conn.cursor() # create a "cursor" 
aircraft_df = pd.read_sql_query("SELECT * FROM seating;", conn) # give the table name and the connection


# ##### Building aircraft, aircraft_left_number, aircraft_left_index DataFrame

# In[30]:

resoverall = pd.DataFrame(c.execute("SELECT DISTINCT seat FROM seating;").fetchall()) # execute a SQL command
columns = resoverall[0].values.tolist()

rows = pd.DataFrame(c.execute("SELECT DISTINCT row FROM seating;").fetchall()) # execute a SQL command
index = rows[0].values.tolist()

data = np.zeros((len(index), len(columns)))
aircraft = pd.DataFrame(data, index=index, columns=columns)
aircraft

#use to get the seat letter after set passager in to airplane
seat_letter = aircraft.columns.values.tolist()
seat_letter[0]

seats_number = len(index)*len(columns)
rows_number = len(index)

seats_located = 0

#aircraft_left_number is used to store the left seats number for each row 
aircraft_left_number = pd.DataFrame(index=aircraft.index,columns = ["left_seats_number"])# setting index as aircraft
aircraft_left_number["left_seats_number"] = len(columns)

aircraft_left_index = pd.DataFrame(index=aircraft.index,columns = ["left_seats_Index"])# setting index as aircraft
aircraft_left_index["left_seats_Index"] = 0

aircraft, aircraft_left_number, aircraft_left_index, seats_located = aircraft_left_number_index(aircraft_df, rows_number, seats_located)


# ##### Read Bookings from CSV

# In[31]:

bookings = pd.read_csv('bookings.csv', header = None)

total_bookings_number = len(bookings)


# #### Main Function to Locate Seats 

# In[32]:

i = 0
refused = 0
separated = 0

# total_bookings_number = 3
max_left_seats_row = aircraft_left_number["left_seats_number"].max()
while(i < total_bookings_number ):
    people_in_group = bookings.iloc[i][1]
    booking_name = bookings.iloc[i][0]
    seats_located += people_in_group
    max_left_seats_row = aircraft_left_number["left_seats_number"].max()
    
#     print(seats_located)
    if seats_located > seats_number: #only refuse when do not have enough seats
        refused += 1                  #otherwise located sepratedly 
        seats_located -= people_in_group
        #update refused and sparated to the database
        update_metrics_table(refused, separated)
    elif seats_located == seats_number: 
        # do the same as seats_located < seats_number:
        if people_in_group <= max_left_seats_row:
            small_than_max(aircraft_left_number, people_in_group, booking_name)
        else:
            separated = bigger_than_max(aircraft_left_number,people_in_group, separated)
        refused += get_total_refused_passagers(i)    
        #update refused and sparated to the database
        update_metrics_table(refused, separated)
        break
    else:
        #seats_located < seats_number
        #locate seats
        if people_in_group <= max_left_seats_row:
            small_than_max(aircraft_left_number, people_in_group, booking_name)
            pd.read_sql_query("SELECT * FROM seating;", conn) # give the table name and the connection
        else:
            separated = bigger_than_max(aircraft_left_number,people_in_group, separated)
            #update to db(refuse_number, seat_away_number)
            update_metrics_table(refused, separated)
    
    
    i += 1
 


# #### Check Results

# In[33]:

aircraft_df = pd.read_sql_query("SELECT * FROM seating;", conn) # give the table name and the connection
aircraft_df


# In[34]:

pd.read_sql_query("SELECT * FROM metrics;", conn)


# In[ ]:



