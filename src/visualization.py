"""
Visualization utilities for the Sales and Profit Performance Dashboard.
This module contains functions for creating data visualizations.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def set_plotting_style():
    """Set the default plotting style for consistent visualizations"""
    sns.set(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12
    
def plot_sales_trend(df, time_column='Order Date', save_path=None):
    """
    Plot sales trend over time
    
    Parameters:
    df (pandas.DataFrame): Input data frame with time and sales columns
    time_column (str): Name of the time column
    save_path (str, optional): Path to save the figure
    
    Returns:
    matplotlib.figure.Figure: The figure object
    """
    set_plotting_style()
    
    # Group by date and calculate daily sales
    if pd.api.types.is_datetime64_any_dtype(df[time_column]):
        sales_by_date = df.groupby(pd.Grouper(key=time_column, freq='M')).agg({
            'Sales': 'sum'
        }).reset_index()
    else:
        return None
    
    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(sales_by_date[time_column], sales_by_date['Sales'], marker='o', linestyle='-')
    
    # Customize the plot
    ax.set_title('Monthly Sales Trend', fontsize=16)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Sales', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save if path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

def plot_profit_margin_by_category(df, save_path=None):
    """
    Plot profit margin by product category
    
    Parameters:
    df (pandas.DataFrame): Input data frame
    save_path (str, optional): Path to save the figure
    
    Returns:
    matplotlib.figure.Figure: The figure object
    """
    set_plotting_style()
    
    if 'Category Name' not in df.columns or 'Profit Margin' not in df.columns:
        return None
    
    # Calculate average profit margin by category
    category_margin = df.groupby('Category Name')['Profit Margin'].mean().sort_values(ascending=False).reset_index()
    
    # Create the plot
    fig, ax = plt.subplots()
    sns.barplot(x='Profit Margin', y='Category Name', data=category_margin, ax=ax)
    
    # Customize the plot
    ax.set_title('Average Profit Margin by Product Category', fontsize=16)
    ax.set_xlabel('Profit Margin', fontsize=14)
    ax.set_ylabel('Category', fontsize=14)
    
    # Add percentage labels
    for i, value in enumerate(category_margin['Profit Margin']):
        ax.text(max(value, 0.01), i, f'{value:.1%}', va='center')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save if path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

def plot_sales_by_region(df, save_path=None):
    """
    Create a bar chart of sales by geographic region
    
    Parameters:
    df (pandas.DataFrame): Input data frame
    save_path (str, optional): Path to save the figure
    
    Returns:
    matplotlib.figure.Figure: The figure object
    """
    set_plotting_style()
    
    if 'Market' not in df.columns or 'Sales' not in df.columns:
        if 'Order Region' in df.columns:
            region_col = 'Order Region'
        else:
            return None
    else:
        region_col = 'Market'
    
    # Group by region and calculate total sales
    sales_by_region = df.groupby(region_col)['Sales'].sum().sort_values(ascending=False).reset_index()
    
    # Create the plot
    fig, ax = plt.subplots()
    sns.barplot(x=region_col, y='Sales', data=sales_by_region, ax=ax)
    
    # Customize the plot
    ax.set_title(f'Total Sales by {region_col}', fontsize=16)
    ax.set_xlabel(region_col, fontsize=14)
    ax.set_ylabel('Sales', fontsize=14)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save if path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig

def create_correlation_heatmap(df, save_path=None):
    """
    Create a correlation heatmap for numeric variables
    
    Parameters:
    df (pandas.DataFrame): Input data frame
    save_path (str, optional): Path to save the figure
    
    Returns:
    matplotlib.figure.Figure: The figure object
    """
    set_plotting_style()
    
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Compute correlation matrix
    corr_matrix = numeric_df.corr()
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    
    # Customize the plot
    ax.set_title('Correlation Heatmap of Numeric Variables', fontsize=16)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save if path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig
