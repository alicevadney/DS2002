import pandas as pd

# 1. reading the csv file
csv = '/Users/alicevadney/Downloads/acc_players-2324F.csv'
acc_players = pd.read_csv(csv)
acc_players = acc_players.dropna()

acc_players.head()
print(acc_players.info)

# 2. basic analysis
total_points = acc_players['PTS'].sum()
print('Total Points:', total_points) # 38411

most_minutes_player = acc_players.loc[acc_players['MP'].idxmax()]
print('Player With the Most Minutes:', most_minutes_player) # Casey Morsell

top_rebounds = acc_players[["Player", "TRB"]].sort_values(by='TRB', ascending=False).head()
print('Five Player With the Most Rebounds:', top_rebounds)

# 3. Player Filtering
over500 = acc_players[acc_players['MP'] > 500]

top_assists = over500[["Player", "AST"]].sort_values(by='AST', ascending = False).head(1)
print('Player With the Most Assists:', top_assists) # Reece Beekman

top3_assists = over500[["Player", "AST"]].sort_values(by='AST', ascending = False).head(3)
print('Three Players With the Most Assists:', top3_assists)

top3_blocks = over500[["Player", "BLK"]].sort_values(by='BLK', ascending = False).head(3)
print('Three Players With the Most Blocks:', top3_assists)

# 4. School-Based Analysis
team_total_points = acc_players.groupby('School')[['PTS']].sum().reset_index()
print('Total Points by School:', team_total_points)

team_total_assists = acc_players.groupby('School')[['AST']].sum().reset_index()
print('Total Assists by School:', team_total_assists)

team_total_points.sort_values(by='PTS', ascending = False).head(3)
print('Top Three Schools by Points:', team_total_points)

# 5. Bonus
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

top5_points = acc_players[["Player", "PTS"]].sort_values(by='PTS', ascending=False).head(5)

plt.figure(figsize=(10, 6))
sns.barplot(x='PTS', y='Player', data=top5_points)
plt.title('Top 5 Players by Total Points')
plt.show()

acc_players["FG%"].corr(acc_players["WS"]) # 0.4334177195258406: yes, there is moderate correlation
plt.figure(figsize=(10, 6))
sns.scatterplot(x='FG%', y='WS', data=acc_players)
plt.title('Field Goal Percentage vs. Win Share')
plt.show()