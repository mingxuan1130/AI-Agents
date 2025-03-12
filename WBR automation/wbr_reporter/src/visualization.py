import matplotlib.pyplot as plt
import pandas as pd

def create_chart(df, chart_path):
    """
    Create a stacked bar chart visualization from the data and save it.
    
    Args:
        df (pandas.DataFrame): DataFrame containing event data with 'event_date', 'category', and 'event_count' columns
        chart_path (str): Path where the chart image will be saved
        
    Returns:
        tuple: (pivot_df, chart_path) - The pivoted DataFrame and path to the saved chart
    """
    # Pivot the data for visualization
    pivot_df = df.pivot(index='event_date', columns='category', values='event_count')
    
    # Create a visualization
    plt.figure(figsize=(12, 8))
    pivot_df.plot(kind='bar', stacked=True)
    plt.title('Events by Category and Date')
    plt.xlabel('Date')
    plt.ylabel('Event Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the chart
    plt.savefig(chart_path)
    
    return pivot_df, chart_path

def get_data_insights(df, pivot_df):
    """
    Generate key insights from the data.
    
    Args:
        df (pandas.DataFrame): Original DataFrame with event data
        pivot_df (pandas.DataFrame): Pivoted DataFrame used for visualization
        
    Returns:
        dict: Dictionary containing key insights about the data
    """
    insights = {
        'total_events': df['event_count'].sum(),
        'date_range': (pivot_df.index.min(), pivot_df.index.max()),
        'most_common_category': {
            'name': df.groupby('category')['event_count'].sum().idxmax(),
            'count': df.groupby('category')['event_count'].sum().max()
        },
        'busiest_date': {
            'date': df.groupby('event_date')['event_count'].sum().idxmax(),
            'count': df.groupby('event_date')['event_count'].sum().max()
        }
    }
    
    return insights 