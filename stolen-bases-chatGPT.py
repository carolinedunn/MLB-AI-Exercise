import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('mlb_teams.csv')

# Filter data from 1900 to 2019 with valid stolen_bases and valid league_id
df_filtered = df[
    (df['year'] >= 1900) & 
    (df['year'] <= 2019) & 
    (df['league_id'].isin(['NL', 'AL'])) & 
    (~df['stolen_bases'].isna())
].copy()

# Create a decade column
df_filtered['decade'] = (df_filtered['year'] // 10) * 10

# Group by league and decade to compute average stolen bases
grouped = df_filtered.groupby(['league_id', 'decade'])['stolen_bases'].mean().reset_index()

# Pivot for plotting
pivot_table = grouped.pivot(index='decade', columns='league_id', values='stolen_bases')

# Plot the results
plt.figure(figsize=(12, 6))
sns.lineplot(data=pivot_table, markers=True, dashes=False)
plt.title('Average Stolen Bases per Team per Year by Decade (1900–2019)')
plt.xlabel('Decade')
plt.ylabel('Average Stolen Bases')
plt.grid(True)
plt.xticks(pivot_table.index)
plt.legend(title='League')
plt.tight_layout()
plt.show()
