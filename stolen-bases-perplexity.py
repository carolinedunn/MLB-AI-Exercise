import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('mlb_teams.csv')

# Filter for years 1900–2019 and NL/AL leagues
df = df[(df['year'] >= 1900) & (df['year'] <= 2019) & (df['league_id'].isin(['NL', 'AL']))]

# Remove rows with missing or non-numeric stolen_bases
df = df[pd.to_numeric(df['stolen_bases'], errors='coerce').notnull()]
df['stolen_bases'] = df['stolen_bases'].astype(float)

# Create a decade column
df['decade'] = (df['year'] // 10) * 10

# Group by league and decade, calculate mean stolen bases per team per year
result = df.groupby(['league_id', 'decade']).agg(
    avg_stolen_bases=('stolen_bases', 'mean')
).reset_index()

# Pivot for plotting
pivot = result.pivot(index='decade', columns='league_id', values='avg_stolen_bases')

# Plot
pivot.plot(kind='bar', figsize=(12,6))
plt.ylabel('Average Stolen Bases per Team per Year')
plt.xlabel('Decade')
plt.title('Average Stolen Bases per Team per Year by Decade (NL vs. AL, 1900–2019)')
plt.legend(title='League')
plt.tight_layout()
plt.show()
