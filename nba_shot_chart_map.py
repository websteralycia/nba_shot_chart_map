#%% #this is how you make a section a jupyter notebook
# https://towardsdatascience.com/make-a-simple-nba-shot-chart-with-python-e5d70db45d0d


from nba_api.stats.endpoints import shotchartdetail
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


# nba_api
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import PlayerCareerStats

# Load teams file
# I want to be able to upload wnba data
teams = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)

# print(type(teams)) -- this is a
# Load players file
players = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)

# example: {'firstName': 'Ivica', 'lastName': 'Zubac', 'playerId': 1627826, 'teamId': 1610612746}
def get_team_id(teams_lookup):
    for team in teams:
      if team['teamName'] == teams_lookup:
        return team['teamId']

# Get player ID based on player name
def get_player_id(first,last):
  for player in players:
   if player['firstName'] == first and player['lastName'] == last:
     return player['playerId']



# Create JSON request
shot_json = shotchartdetail.ShotChartDetail(
              team_id = get_team_id('Golden State Warriors'),
              player_id = get_player_id('Stephen', 'Curry'),
              context_measure_simple = 'PTS',
              season_nullable = '2015-16',
              season_type_all_star = 'Regular Season')

  # # # Load data into a Python dictionary
shot_data = json.loads(shot_json.get_json())
# print(shot_data)
print(shot_data.keys())
# Get the relevant data from our dictionary
relevant_data = shot_data['resultSets'][0]

# print(relevant_data)

print(relevant_data.keys()) # dict_keys(['name', 'headers', 'rowSet']) all keys resultSets 0 aka relevant data we then want the headers and row set 

#   # Get the headers and row data
headers = relevant_data['headers']
rows = relevant_data['rowSet']

#   # Create pandas DataFrame
#Put this data together into a pandas DataFrame, which is as simple as the following:
curry_data = pd.DataFrame(rows) # entire spreadsheet like data 
curry_data.columns = headers # this just takes the column headers from curry_data 

print(curry_data)
# print(curry_data.columns) # this just take




#   # Function to draw basketball court
def create_court(ax, color):



#   # # Short corner 3PT lines
  ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
  ax.plot([220, 220], [0, 140], linewidth=2, color=color)

#   # 3PT Arc
  ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))

#   # Lane and Key
  ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
  ax.plot([80, 80], [0, 190], linewidth=2, color=color)
  ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
  ax.plot([60, 60], [0, 190], linewidth=2, color=color)
  ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
  ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))

#   # Rim
  ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))
      
#   # Backboard
  ax.plot([-30, 30], [40, 40], linewidth=2, color=color)

#   # Remove ticks
  ax.set_xticks([])
  ax.set_yticks([])
      
  # Set axis limits
  ax.set_xlim(-250, 250)
  ax.set_ylim(0, 470)

  # General plot parameters ## This needs to be outside of the function ## a test, may have to remove for real thing 
mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2

  # Draw basketball court ## This needs to be outside of the function
fig = plt.figure(figsize=(4, 3.76))
ax = fig.add_axes([0, 0, 1, 1])
# hexbin = plt.hexbin(curry_data['LOC_X'], curry_data['LOC_Y'] + 60, gridsize=(30, 30), extent=(-300, 300, 0, 940), bins='log', cmap='plasma_r')
hexbin_log_binning = plt.hexbin(curry_data['LOC_X'], curry_data['LOC_Y'] + 60, gridsize=(30, 30), extent=(-300, 300, 0, 940), bins='log', cmap='copper_r')
# I like coolwarm, terrain, gist_earth_r
# ax.set_facecolor('tan') how to set background color 
ax = create_court(ax, 'black')
plt.show()

# # Setting the background color of the plot
# # using set_facecolor() method
# ax.set_facecolor("yellow")  HOW TO SET BACKGROUND COLOR









