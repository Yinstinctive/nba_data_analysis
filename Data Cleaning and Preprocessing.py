import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

player_data = pd.read_csv(r'C:\Users\yingk\Desktop\nba-players-stats\player_data.csv')
player_data.columns
player_data.drop(['birth_date', 'college'], axis=1, inplace=True)

#check missing value
player_data.describe()
player_data.isna().sum()
player_data.dropna(inplace=True)

player_data.head(20)

#transform postions
def transform_position(value):
    if value=='F-C':
        return 'F'
    elif value=='G-F':
        return 'G'
    elif value =='C-F':
        return 'C'
    elif value =='F-G':
        return 'F'
    else:
        return value
print('initial position distribution')
print(player_data['position'].value_counts())
player_data['position'] = player_data['position'].apply(transform_position)
print('transformed position distribution')
print(player_data['position'].value_counts())

def transform_height(height):
    h = height.split('-')
    feet = float(h[0])
    inch = float(h[1])
    meters = 0.3048*feet+0.0254*inch
    return meters
player_data['height_in_meters'] = player_data['height'].apply(transform_height)

#player_data.to_csv(r'transformed_player_data.csv')

#C_data = player_data[player_data['position']=='C']
#F_data = player_data[player_data['position']=='F']
#G_data = player_data[player_data['position']=='G']
#
#C_mean_byYear = C_data.groupby('year_start').mean()
#F_mean_byYear = F_data.groupby('year_start').mean()
#G_mean_byYear = G_data.groupby('year_start').mean()

#Read data
season_data = pd.read_csv(r'Seasons_Stats.csv')
season_data.head()
champion_data = pd.read_csv(r'Champion_Record.csv')
champion_data.head()
champion_data.dtypes
#Start from 1982
filtered_season_data = season_data[season_data['Year']>=1982].copy()
#Create unique Id for each team each season
champion_data['Id'] = champion_data['Year'].astype(str)+champion_data['Champion_Team']
filtered_season_data['Id'] = filtered_season_data['Year'].astype(str)+filtered_season_data['Tm']
filtered_season_data['Id'] = filtered_season_data['Id'].apply(lambda Id:Id.split('.0')[0]+Id.split('.0')[1])
filtered_season_data.to_csv(r'filtered_season_data.csv')
#Gather Top 10 assiting player data
ast_pts = filtered_season_data.loc[:,['Year','Player','Pos','G','AST','PTS']].copy()
ast_pts['Avg_Ast'] = ast_pts['AST']/ast_pts['G']
ast_pts['Avg_Pts'] = ast_pts['PTS']/ast_pts['G']
topAst_df = pd.DataFrame(columns = ast_pts.columns)
for year in range(1982,2018):
    part = ast_pts[ast_pts['Year']==year].nlargest(10,columns='AST')
    topAst_df = pd.concat([topAst_df,part])
topAst_df.to_csv(r'topAst.csv')
#Mark champion team for each season    
def is_champion(value):
    if value in list(champion_data['Id']):
        return 1
    return 0
filtered_season_data['Champion'] = filtered_season_data['Id'].apply(is_champion)
champion_teams = filtered_season_data[filtered_season_data['Champion']==1].copy()
champion_teams.to_csv(r'champion_teams.csv')

#Group by team, both champion and non-champion
stats = filtered_season_data[['Id','Champion','FG','FGA','3P','3PA','2P','2PA','FT','FTA','ORB','DRB','AST','STL','BLK','TOV','PF','PTS']].copy()
stats_by_team = stats.groupby('Id').sum()
stats_by_team.head()
stats_by_team['Champion'] = stats_by_team['Champion'].apply(lambda c:1 if c!=0 else c)
stats_by_team.reset_index(inplace=True)
stats_by_team.columns
stats_by_team['Year'] = stats_by_team['Id'].apply(lambda i:i[0:4])

champion_stats = stats_by_team[stats_by_team['Champion']==1].copy()
non_champion_stats = stats_by_team[stats_by_team['Champion']==0].copy().groupby('Year').mean()
#non_champion_stats.reset_index(inplace=True)
champion_stats.drop(['Id'],axis=1,inplace=True)
champion_stats.set_index('Year',inplace=True)
champion_stats.columns
non_champion_stats.columns
#Create dataframe calculating the difference between champion and non-champion team
df = pd.DataFrame(columns=champion_stats.columns)
for year in range(1982,2018):
    value = []
    for column in champion_stats.columns:
        v = (champion_stats[column][f'{year}']-non_champion_stats[column][f'{year}'])
        if year==1999:
            v=v/50
        elif year==2012:
            v=v/66
        else:
            v=v/82
        value.append(v)
    df2 = pd.DataFrame([value],index=[f'{year}'],columns=champion_stats.columns)
    df = pd.concat([df,df2])
df.drop(['Champion'],axis=1,inplace=True)
df.reset_index(inplace=True)
df.rename(columns={'index':'Year'},inplace=True)
df.to_csv(r'champion_subtract_non.csv')

#rate = stats_by_team.corr()
#print(rate.iloc[0,:])
#plt.figure(figsize=(6,5),dpi=100)
#sns.heatmap(rate,cmap='coolwarm',linewidths=0.5)

#stats_by_team.to_csv(r'basic_team_stats.csv')