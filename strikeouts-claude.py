import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def analyze_mlb_strikeouts(file_path):
    """
    Analyze MLB strikeouts by pitchers, comparing NL vs AL by decade.
    
    Args:
        file_path (str): Path to the MLB teams CSV file
    """
    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded data with {len(df)} rows")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return
    
    # Create decade column
    df['decade'] = (df['year'] // 10) * 10
    df['decade_label'] = df['decade'].astype(str) + 's'
    
    # Check if data contains required columns
    required_cols = ['year', 'league_id', 'strikeouts_by_pitchers', 'team_name']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Warning: Missing required columns: {missing_cols}")
        print("Available columns:", df.columns.tolist())
    
    # Create summary dataframe with average strikeouts by pitchers per team by decade and league
    if 'strikeouts_by_pitchers' in df.columns and 'league_id' in df.columns:
        # Group by decade and league, calculating average strikeouts
        decade_summary = df.groupby(['decade_label', 'league_id'])['strikeouts_by_pitchers'].agg(
            avg_strikeouts=('mean'),
            team_count=('count')
        ).reset_index()
        
        # Pivot the data to get NL and AL as separate columns
        pivot_df = decade_summary.pivot(
            index='decade_label', 
            columns='league_id', 
            values=['avg_strikeouts', 'team_count']
        ).reset_index()
        
        # Flatten hierarchical column names
        pivot_df.columns = ['_'.join(col).strip('_') for col in pivot_df.columns.values]
        
        # Create a more readable dataframe for display
        result_df = pd.DataFrame({
            'Decade': pivot_df['decade_label'],
            'NL_Avg_Strikeouts': pivot_df.get('avg_strikeouts_NL', np.nan),
            'AL_Avg_Strikeouts': pivot_df.get('avg_strikeouts_AL', np.nan),
            'NL_Teams': pivot_df.get('team_count_NL', 0),
            'AL_Teams': pivot_df.get('team_count_AL', 0)
        })
        
        # Sort by decade
        result_df['Decade_Sort'] = result_df['Decade'].str.extract('(\d+)').astype(int)
        result_df = result_df.sort_values('Decade_Sort').drop('Decade_Sort', axis=1)
        
        # Round average strikeouts to 1 decimal place
        if 'NL_Avg_Strikeouts' in result_df.columns:
            result_df['NL_Avg_Strikeouts'] = result_df['NL_Avg_Strikeouts'].round(1)
        if 'AL_Avg_Strikeouts' in result_df.columns:
            result_df['AL_Avg_Strikeouts'] = result_df['AL_Avg_Strikeouts'].round(1)
        
        # Print summary table
        print("\nAverage Strikeouts by Pitchers Per Team By Decade and League:")
        print(result_df.to_string(index=False))
        
        # Create visualization
        create_visualization(result_df)
        
        return result_df
    else:
        print("Required data columns missing. Available columns:", df.columns.tolist())
        return None

def create_visualization(df):
    """
    Create a bar chart visualization comparing NL vs AL strikeouts by decade.
    
    Args:
        df (DataFrame): Processed data with decade averages
    """
    # Set up the visualization style
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("colorblind")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Get decades for x-axis
    decades = df['Decade'].tolist()
    x = np.arange(len(decades))
    width = 0.35
    
    # Create bars
    nl_data = df['NL_Avg_Strikeouts'].fillna(0).tolist()
    rects1 = ax.bar(x - width/2, nl_data, width, label='National League')
    
    # Add AL data if available
    if 'AL_Avg_Strikeouts' in df.columns:
        al_data = df['AL_Avg_Strikeouts'].fillna(0).tolist()
        rects2 = ax.bar(x + width/2, al_data, width, label='American League')
    
    # Add labels, title and legend
    ax.set_xlabel('Decade', fontsize=12)
    ax.set_ylabel('Average Strikeouts by Pitchers per Team', fontsize=12)
    ax.set_title('MLB Average Strikeouts by Pitchers Per Team: NL vs AL by Decade', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(decades)
    ax.legend()
    
    # Add data labels on bars
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f'{height}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom')
    
    add_labels(rects1)
    if 'AL_Avg_Strikeouts' in df.columns:
        add_labels(rects2)
    
    # Add data note for sample data
    if len(decades) == 1 and decades[0] == '1870s':
        plt.figtext(0.5, 0.01, 
                   "Note: Sample data only includes NL teams from 1876-1878.\nThe American League (AL) was officially formed in 1901.",
                   ha="center", fontsize=10, bbox={"facecolor":"lightgrey", "alpha":0.5, "pad":5})
    
    plt.tight_layout()
    
    # Save the visualization
    plt.savefig('mlb_strikeouts_by_decade.png', dpi=300, bbox_inches='tight')
    print("Visualization saved as 'mlb_strikeouts_by_decade.png'")
    
    # Show the plot
    plt.show()

# Example usage
if __name__ == "__main__":
    # Replace with your actual file path
    file_path = "mlb_teams.csv"
    analyze_mlb_strikeouts(file_path)