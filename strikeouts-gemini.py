import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataframe.
df = pd.read_csv('mlb_teams.csv')

# Calculate the decade for each year using the 'year' column.
df['decade'] = (df['year'] // 10) * 10

# Group by decade and league_id and calculate the average pitcher strikeouts for the entire decade.
decade_league_avg_strikeouts = df.groupby(['decade', 'league_id'])['strikeouts_by_pitchers'].mean().reset_index()

# Print the summary table (optional, but can be helpful).
print("Average Pitcher Strikeouts by League and Decade (Table):")
summary_by_decade_table = decade_league_avg_strikeouts.pivot(index='league_id', columns='decade', values='strikeouts_by_pitchers')
print(summary_by_decade_table)
print("\n" + "="*50 + "\n") # Separator

# Create a grouped bar chart.
plt.figure(figsize=(12, 7)) # Adjust figure size as needed
sns.barplot(
    data=decade_league_avg_strikeouts,
    x='decade',
    y='strikeouts_by_pitchers',
    hue='league_id',
    palette='viridis' # Optional: choose a color palette
)

# Add titles and labels to the chart.
plt.title('Average Pitcher Strikeouts by League and Decade', fontsize=16)
plt.xlabel('Decade', fontsize=12)
plt.ylabel('Average Strikeouts by Pitchers', fontsize=12)
plt.xticks(rotation=45, ha='right') # Rotate x-axis labels for better readability
plt.legend(title='League')
plt.grid(axis='y', linestyle='--', alpha=0.7) # Add a horizontal grid for readability

# Adjust layout and display the plot.
plt.tight_layout()
plt.show()