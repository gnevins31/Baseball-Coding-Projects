#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 17:15:34 2024

@author: gnevins
"""


import pandas as pd
import numpy as np
import pybaseball as pyb
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup

                                                             

all_data = pyb.pitching_stats(start_season=2021,end_season=2024,qual=0)

rodon_data_pybaseball = all_data.query("Name == 'Carlos Rodon'")
                                                              
for column in rodon_data_pybaseball.columns:
    print(column)
    
rodon_pitch_usage = rodon_data_pybaseball[['Season','FA% (sc)','SL% (sc)','CH% (sc)']].sort_values('Season')


#Pitch Usage Line Graph
fastball_plot = sns.lineplot(data=rodon_pitch_usage,x='Season',y='FA% (sc)',marker='o',label='Fastball')
slider_plot = sns.lineplot(data=rodon_pitch_usage,x='Season',y='SL% (sc)',marker='o',label='Slider')
changeup_plot = sns.lineplot(data=rodon_pitch_usage,x='Season',y='CH% (sc)',marker='o',label='Changeup')


for i, j in zip(rodon_pitch_usage['Season'], rodon_pitch_usage['FA% (sc)']):
    plt.annotate(str(round(j, 2)), xy=(i-.07, j-.05))

for i, j in zip(rodon_pitch_usage['Season'], rodon_pitch_usage['SL% (sc)']):
    plt.annotate(str(round(j, 2)), xy=(i-.07, j+.02))

for i, j in zip(rodon_pitch_usage['Season'], rodon_pitch_usage['CH% (sc)']):
    plt.annotate(str(round(j, 2)), xy=(i-.07, j+.02))
    

plt.xticks([2021,2022,2023,2024])
plt.ylabel('Pitch Usage')
plt.legend(loc='upper center',fontsize = 10,bbox_to_anchor=(1.15, 0.7))
plt.title('Pitch Usage by Year')


# Web Scraping Baseball Savant
url = "https://baseballsavant.mlb.com/savant-player/carlos-rodon-607074?stats=statcast-r-pitching-mlb"

html = requests.get(url)

soup_version = BeautifulSoup(html.text)

table = soup_version.find_all('table')[45]

headers = [th.text.strip() for th in table.find_all('th')]

data = []
for row in table.find_all('tr'):
    row_data = [td.text.strip() for td in row.find_all('td')]
    data.append(row_data)

df = pd.DataFrame(data, columns=headers)
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['xwOBA'] = pd.to_numeric(df['xwOBA'], errors='coerce')
df = df.query("Year > 2020")[['Year','Pitch Type','xwOBA']]
df = df.query("`Pitch Type` in ['4-Seam Fastball','Slider','Changeup']")


# xERA by pitch type by year graph
xwOBA_graph = sns.lineplot(data=df,x='Year',y='xwOBA',hue='Pitch Type',marker='o')

plt.xticks([2021,2022,2023,2024])
plt.ylabel('xwOBA')
plt.legend(loc='upper center',fontsize = 10,bbox_to_anchor=(1.25, 0.7))
plt.title('xwOBA by Pitch Type by Year')

for i, j in zip(df['Year'], df['xwOBA']):
    plt.annotate(str(round(j, 3)), xy=(i+.07, j))

    

    













