#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 14:55:04 2024

@author: Gregory Nevins
"""


import pandas as pd
import numpy as np
import pybaseball as pyb
import matplotlib.pyplot as plt
import seaborn as sns

                                           
def player_data(last_name,first_name):
    """
    
    Parameters
    ----------
    last_name : string (Case Insensitive)
        player's last name.
    first_name : string (Case Insensitive)
        player's first name.

    Returns
    -------
    player_2023_data : DataFrame
        2023 data DataFrame.
        
    """
    
    player_id = int(pyb.playerid_lookup(last_name,first_name)['key_mlbam'])
    
    # Filter data to only include events with batted ball information
    player_2023_data = pyb.statcast_batter('2023-03-30','2023-10-01',player_id)\
    .query("events in ['single','field_out','double',\
    'grounded_into_double_play','field_error','force_out','home_run','triple','sac_fly',\
    'fielders_choice_out']")
    
    
    return player_2023_data


filtered_2023_data = player_data('Volpe','Anthony')                                                                 
                                           
                                                                                                                                                                                                                                       
sns.lmplot(
    data=filtered_2023_data,
    x="launch_angle",
    y="launch_speed",
).set(title='Anthony Volpe 2023 LA vs. EV')

plt.axvline(x=8, color='black', linestyle='--')
plt.axvline(x=25, color='black', linestyle='--')


sns.relplot(
    data=filtered_2023_data,
    x="launch_angle",
    y="hit_distance_sc",
    hue="events",
).set(title='Anthony Volpe LA vs. Hit Distance 2023')
                               
plt.axvline(x=25, color='black', linestyle='--')
                               

sns.relplot(
    data=filtered_2023_data,
    x="launch_speed",
    y="hit_distance_sc",
    hue="events"
).set(title='Anthony Volpe 2023 EV vs. Hit Distance 2023')

                          
sns.lmplot(
    data=filtered_2023_data.query("hit_distance_sc > 100"),
    x="launch_speed",
    y="hit_distance_sc",
).set(title='Anthony Volpe 2023 EV vs. Hit Distance (>100 feet distance)')


# Correlation Matrix
filtered_2023_data[['launch_angle','launch_speed','hit_distance_sc']].corr()

# Correlation Matrix with data points > 100 feet in distance
(filtered_2023_data[['launch_angle','launch_speed','hit_distance_sc']].query
("hit_distance_sc > 100")).corr()




