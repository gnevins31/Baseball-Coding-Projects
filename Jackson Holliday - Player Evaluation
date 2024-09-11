#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 17:30:04 2024

@author: Gregory Nevins
"""

import matplotlib.pyplot as plt
import numpy as np
import pybaseball as pyb
from datetime import date
import pandas as pd
import seaborn as sns



pitch_type_groups = {
    'fastball': ['FF', 'SI', 'FC'],
    'breaking': ['SL', 'CU', 'ST', 'SV', 'KC'],
    'offspeed': ['FS', 'CH']
}

descriptions = {
    'in play': ['hit_into_play'],
    'swinging strike': ['swinging_strike','swinging_strike_blocked','foul_tip'],
    'called strike': ['called_strike'],
    'foul': ['foul'],
    'ball':['ball','blocked_ball'],
    'hit by pitch': ['hit_by_pitch'],
    'swing': ['hit_into_play','swinging_strike','swinging_strike_blocked','foul_tip','foul']
    }

pitch_colors_dict = {'swinging_strike': 'red',
 'foul_tip': 'red',
 'swinging_strike_blocked': 'red',
 'ball': 'blue',
 'blocked_ball': 'blue',
 'hit_into_play': 'green',
 'called_strike': 'orange',
 'foul': 'purple',
 'foul_bunt': 'purple',
 'hit_by_pitch': 'brown'}


def create_strike_zone(start_date, end_date, last_name, first_name, ax=plt.gca()):
    """
    Create a strike zone plot for a specific player based on their strike zone dimensions.

    Parameters
    ----------
    start_date : str
        First day to start collecting data (YYYY-MM-DD format)
    end_date : str
        Last day to collect data (YYYY-MM-DD format)
    last_name : str
        Player's last name (case insensitive)
    first_name : str
        Player's first name (case insensitive)
    ax : matplotlib Axes, optional
        Axes object on which to draw the strike zone plot. If not provided, uses the current axes instance.

    Returns
    -------
    ax : matplotlib Axes
        Axes object with the strike zone plot drawn on it.

    """
    
    # Home plate as a pentagon
    home_plate = plt.Polygon([
        (0, -0.25),          
        (-0.708, 0.292),  
        (-0.708, .8),  
        (0.708, .8),  
        (0.708, 0.292)  
    ], closed=True, fill=None, edgecolor='black')
    ax.add_patch(home_plate)
    
    # Strike zone 
    strike_zone_top = player_data_filtered(start_date, end_date, last_name, first_name)['sz_top'].mean()
    strike_zone_bot = player_data_filtered(start_date, end_date, last_name, first_name)['sz_bot'].mean()
    
    strike_zone = plt.Rectangle((-0.708, strike_zone_bot), 1.417, strike_zone_top-strike_zone_bot, 
                                fill=None, edgecolor='black')
    ax.add_patch(strike_zone)
    
    # Axis limits and labels
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1, 5)
    ax.set_aspect('equal')
    ax.set_title(f"Strike Zone for {first_name} {last_name}",fontsize=14)
    ax.set_xlabel("Distance from center of plate (feet)",fontsize=14)
    ax.set_ylabel("Height (feet)",fontsize=14)
    
    return ax



def player_id(last_name,first_name):
    """
    Look up a player's MLB ID based on their last name and first name.

    Parameters
    ----------
    last_name : str
        Player's last name (case insensitive)
    first_name : str
        Player's first name (case insensitive)

    Returns
    -------
    int
        The player's ID in MLB Advanced Media (MLBAM) format

    """
    
    return int(pyb.playerid_lookup(last_name,first_name)['key_mlbam'])



def player_data_all_columns(start_date,end_date,last_name,first_name):
    """
    Retrieve player data for a specific player within a given date range.

    Parameters
    ----------
    start_date : str
        First day to start collecting data (YYYY-MM-DD format)
    end_date : str
        Last day to collect data (YYYY-MM-DD format)
    last_name : str
        Player's last name (case insensitive)
    first_name : str
        Player's first name (case insensitive)

    Returns
    -------
    pandas.DataFrame
        A dataframe containing the player's data for the specified date range

    """
    
    playerid = player_id(last_name,first_name)
    
    return pyb.statcast_batter(start_date,end_date,playerid)



def player_data_filtered(start_date, end_date, last_name, first_name, pitch_type='all', 
                         pitch_description = 'all', pitcher_handedness = 'all'):
    """
    Retrieve and filter player data based on various criteria.

    Parameters
    ----------
    start_date : str
        First day to start collecting data (YYYY-MM-DD format)
    end_date : str
        Last day to collect data (YYYY-MM-DD format)
    last_name : str
        Player's last name (case insensitive)
    first_name : str
        Player's first name (case insensitive)
    pitch_type : str, optional (default='all')
        Types of pitches (fastball, breaking, offspeed)
    pitch_description : str, optional (default='all')
        Pitch description (in play, swinging strike, called strike, foul, ball, hit by pitch, swing)
    pitcher_handedness : str, optional (default='all')
        Pitcher handedness (L or R)

    Returns
    -------
    pandas.DataFrame
        A filtered dataframe of player data based on the specified criteria

    """
    playerid = player_id(last_name, first_name)
    
    columns = [
        'game_date', 'pitch_type', 'description', 'events', 'release_speed', 'p_throws',
        'batter', 'pitcher', 'home_team', 'away_team', 'balls', 'strikes', 'bb_type', 
        'plate_x', 'plate_z', 'sz_top', 'sz_bot', 'hit_distance_sc','launch_speed','launch_angle',
        'estimated_woba_using_speedangle','woba_value']
    
    data = pyb.statcast_batter(start_date, end_date, playerid)[columns]
    
    
    if pitch_type in pitch_type_groups:
        data = data[data['pitch_type'].isin(pitch_type_groups[pitch_type])]
        
    if pitch_description in descriptions:
        data = data[data['description'].isin(descriptions[pitch_description])]
        
    if pitcher_handedness in ['L','R']:
        data = data[data['p_throws'] == pitcher_handedness]
    
    return data



def player_data_strike_zone(start_date,end_date,last_name,first_name,pitch_type = 'all',
                            pitch_description = 'all', pitcher_handedness = 'all'):
    """
    Generate a strike zone plot with filtered data points.

    Parameters
    ----------
    start_date : str
        First day to start collecting data (YYYY-MM-DD format)
    end_date : str
        Last day to collect data (YYYY-MM-DD format)
    last_name : str
        Player's last name (case insensitive)
    first_name : str
        Player's first name (case insensitive)
    pitch_type : str, optional (default='all')
        Types of pitches (fastball, breaking, offspeed)
    pitch_description : str, optional (default='all')
        Pitch description (in play, swinging strike, called strike, foul, ball, hit by pitch, swing)
    pitcher_handedness : str, optional (default='all')
        Pitcher handedness (L or R)

    Returns
    -------
    matplotlib Axes
        A strike zone plot with filtered data points

    """
    fig, ax = plt.subplots(figsize=(8,10))
    player_data = player_data_filtered(start_date, end_date, last_name, first_name, 
                             pitch_type, pitch_description, pitcher_handedness)
    print(player_data)
        
    sns.scatterplot(x="plate_x", y="plate_z", hue="description", data=player_data, palette=pitch_colors_dict, ax=ax)
    
    create_strike_zone(start_date, end_date, last_name, first_name, ax)
    
    return ax


# 1st stint data collection
first_stint_data = player_data_filtered('2024-04-10','2024-04-23','Holliday','Jackson')
first_stint_xwoba = first_stint_data['estimated_woba_using_speedangle'].mean()
first_stint_xwoba_fastball = player_data_filtered('2024-04-10','2024-04-23','Holliday',
                'Jackson','fastball')['estimated_woba_using_speedangle'].mean()

first_stint_xwoba_breaking = player_data_filtered('2024-04-10','2024-04-23','Holliday',
                'Jackson','breaking')['estimated_woba_using_speedangle'].mean()

first_stint_xwoba_offspeed = player_data_filtered('2024-04-10','2024-04-23','Holliday',
                'Jackson','offspeed')['estimated_woba_using_speedangle'].mean()

# Bar graph showing first stint xwOBA values
data_graph = {'pitch_type': ['MLB AVG','Overall','Fastball', 'Breaking', 'Offspeed'],
        'xwoba': [.315,first_stint_xwoba, first_stint_xwoba_fastball, first_stint_xwoba_breaking, 
                  first_stint_xwoba_offspeed]}
df = pd.DataFrame(data_graph).set_index('pitch_type')

plt.figure(figsize=(8,6))
ax = sns.barplot(x=df.index, y=df['xwoba'])

plt.xlabel('Pitch Type', fontweight='bold', fontsize=14)
plt.ylabel('xwOBA', fontweight='bold', fontsize=14)
plt.title('xwOBA by Pitch Type -- First Stint (4/10/24 -- 4/23/24)', fontweight='bold', fontsize=14)

ax.bar_label(ax.containers[0], labels=[format(val, '.3f') for val in df['xwoba']], 
             label_type='center', fontweight='bold', fontsize=14, color='white')

plt.xticks(fontsize=14)  
plt.yticks(fontsize=12)  


# Whiff rates by pitch type -- First Stint
overall_whiff_rate = round((len(player_data_filtered('2024-04-10','2024-04-23',
                    'Holliday','Jackson',pitch_description='swinging strike')) / 
                     len(player_data_filtered('2024-04-10','2024-04-23','Holliday',
                    'Jackson',pitch_description='swing'))) * 100,2)

fastball_whiff_rate = round((len(player_data_filtered('2024-04-10','2024-04-23',
                    'Holliday','Jackson','fastball','swinging strike')) / 
                     len(player_data_filtered('2024-04-10','2024-04-23','Holliday',
                    'Jackson','fastball','swing'))) * 100,2)

breaking_whiff_rate = round((len(player_data_filtered('2024-04-10','2024-04-23',
                    'Holliday','Jackson','breaking','swinging strike')) / 
                     len(player_data_filtered('2024-04-10','2024-04-23','Holliday',
                    'Jackson','breaking','swing'))) * 100,2)

offspeed_whiff_rate = round((len(player_data_filtered('2024-04-10','2024-04-23',
                    'Holliday','Jackson','offspeed','swinging strike')) / 
                     len(player_data_filtered('2024-04-10','2024-04-23','Holliday',
                    'Jackson','offspeed','swing'))) * 100,2)

whiff_rates_graph = {'pitch_type': ['MLB AVG','Overall','Fastball', 'Breaking', 'Offspeed'],
        'whiff_rate': [24.9,overall_whiff_rate, fastball_whiff_rate, breaking_whiff_rate, offspeed_whiff_rate]}
df = pd.DataFrame(whiff_rates_graph).set_index('pitch_type')

plt.figure(figsize=(8,6))
ax = sns.barplot(x=df.index, y=df['whiff_rate'])

plt.xlabel('Pitch Type',fontweight='bold',fontsize=14)
plt.ylabel('Whiff Rate %',fontweight='bold',fontsize=14)
plt.title('Whiff Rate by Pitch Type -- First Stint (4/10/24 -- 4/23/24)',fontweight='bold',fontsize=14)

ax.bar_label(ax.containers[0], labels=[f'{val:.2f} %' for val in df['whiff_rate']], 
             label_type='center', fontweight='bold', fontsize=14, color='white')

plt.xticks(fontsize=14)  
plt.yticks(fontsize=12)  

# First Stint Fastballs plot
fastball_first_stint_swings_plot = player_data_strike_zone('2024-04-10', '2024-04-23', 
                    'Holliday', 'Jackson', 'fastball', 'swing').set(
                    title='Jackson Holliday Swings on Fastballs -- First Stint')
                        
fastball_first_stint_whiffs_plot = player_data_strike_zone('2024-04-10', '2024-04-23', 
                    'Holliday', 'Jackson', 'fastball', 'swinging strike').set(
                     title='Jackson Holliday Fastball Whiffs -- First Stint')



# 2nd stint data collection
second_stint_data = player_data_filtered('2024-07-31','2024-09-04','Holliday','Jackson')
second_stint_xwoba = second_stint_data['estimated_woba_using_speedangle'].mean()
second_stint_xwoba_fastball = player_data_filtered('2024-07-31','2024-09-04','Holliday',
                'Jackson','fastball')['estimated_woba_using_speedangle'].mean()

second_stint_xwoba_breaking = player_data_filtered('2024-07-31','2024-09-04','Holliday',
                'Jackson','breaking')['estimated_woba_using_speedangle'].mean()

second_stint_xwoba_offspeed = player_data_filtered('2024-07-31','2024-09-04','Holliday',
                'Jackson','offspeed')['estimated_woba_using_speedangle'].mean()

# Bar graph comparing first and second stint xwOBA values
data_graph = {'pitch_type': ['MLB AVG','Overall','Fastball', 'Breaking', 'Offspeed'],
              'First Stint': [.315,first_stint_xwoba, first_stint_xwoba_fastball, 
                             first_stint_xwoba_breaking, first_stint_xwoba_offspeed],
              'Second Stint': [.315,second_stint_xwoba, second_stint_xwoba_fastball, 
                              second_stint_xwoba_breaking, second_stint_xwoba_offspeed]}

df = pd.DataFrame(data_graph)

df_melted = pd.melt(df, id_vars=['pitch_type'], var_name='Stint', value_name='xwOBA')

plt.figure(figsize=(8,6))
ax = sns.barplot(x='pitch_type', y='xwOBA', hue='Stint', data=df_melted)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2, p.get_height()/2, '{:.3f}'.format(p.get_height()), 
    ha='center', va='center', size=11, color='white',fontweight='bold')

plt.xlabel('Pitch Type', fontweight='bold', fontsize=14)
plt.ylabel('xwOBA', fontweight='bold', fontsize=14)
plt.title('xwOBA by Pitch Type -- Both Stints', fontweight='bold', fontsize=14)

plt.legend(title='Stint', fontsize=12)
plt.xticks(fontsize=14)  
plt.yticks(fontsize=12)  


# Whiff rates by pitch type -- Comparing first and second stint values
second_stint_overall_whiff_rate = round((len(player_data_filtered('2024-07-31','2024-09-04','Holliday',
                'Jackson',pitch_description='swinging strike')) / len(player_data_filtered('2024-07-31',
                '2024-09-04','Holliday','Jackson',pitch_description='swing'))) * 100,2)
                                                                                           
second_fastball_whiff_rate = round((len(player_data_filtered('2024-07-31','2024-09-04',
                'Holliday','Jackson','fastball','swinging strike')) / len(player_data_filtered('2024-07-31',
                '2024-09-04','Holliday','Jackson','fastball','swing'))) * 100,2)
                                                                                               
second_breaking_whiff_rate = round((len(player_data_filtered('2024-07-31','2024-09-04','Holliday',
                'Jackson','breaking','swinging strike')) / len(player_data_filtered('2024-07-31',
                '2024-09-04','Holliday','Jackson','breaking','swing'))) * 100,2)
                                                                                    
second_offspeed_whiff_rate = round((len(player_data_filtered('2024-07-31','2024-09-04','Holliday',
                'Jackson','offspeed','swinging strike')) / len(player_data_filtered('2024-07-31',
                '2024-09-04','Holliday','Jackson','offspeed','swing'))) * 100,2)

whiff_rates_graph = {'stint': ['First Stint', 'First Stint', 'First Stint', 'First Stint', 'First Stint', 
                    'Second Stint', 'Second Stint', 'Second Stint', 'Second Stint', 'Second Stint'],
                    'pitch_type': ['MLB AVG', 'Overall', 'Fastball', 'Breaking', 'Offspeed', 'MLB AVG', 
                    'Overall', 'Fastball', 'Breaking', 'Offspeed'],
                    'whiff_rate': [24.9, overall_whiff_rate, fastball_whiff_rate, breaking_whiff_rate, 
                                  offspeed_whiff_rate, 24.9, second_stint_overall_whiff_rate, 
                                  second_fastball_whiff_rate, second_breaking_whiff_rate, 
                                  second_offspeed_whiff_rate]}

df = pd.DataFrame(whiff_rates_graph)

# Create the graph
plt.figure(figsize=(10,6))
ax = sns.barplot(x="pitch_type", y="whiff_rate", hue="stint", data=df)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2, p.get_height()/2, '{:.2g}%'.format(p.get_height()), 
    ha='center', va='center', fontweight='bold', fontsize=14, color='white')

plt.xlabel('Pitch Type', fontweight='bold', fontsize=14)
plt.ylabel('Whiff Rate %', fontweight='bold', fontsize=14)
plt.title('Whiff Rate by Pitch Type -- Both Stints', fontweight='bold', fontsize=14)
plt.legend(title='Stint', loc='upper right', fontsize=12)
plt.xticks(fontsize=14)  
plt.yticks(fontsize=12) 


# Second Stint Fastballs plot
fastball_second_stint_swings_plot = player_data_strike_zone('2024-07-31', '2024-09-04', 'Holliday', 
                  'Jackson', 'fastball', 'swing').set(
                   title='Jackson Holliday Swings on Fastballs -- Second Stint')
                      
fastball_second_stint_whiffs_plot = player_data_strike_zone('2024-07-31', '2024-09-04', 'Holliday', 
                  'Jackson', 'fastball', 'swinging strike').set(
                   title='Jackson Holliday Fastball Whiffs -- Second Stint')
