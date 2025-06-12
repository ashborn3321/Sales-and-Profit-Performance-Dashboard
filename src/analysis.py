"""
Analysis utilities for the Sales and Profit Performance Dashboard.
This module contains functions for analyzing sales and profit data.
"""

import pandas as pd
import numpy as np

def calculate_summary_stats(df):
    """
    Calculate summary statistics for sales and profit data
    
    Parameters:
    df (pandas.DataFrame): Input data frame
    
    Returns:
    dict: Dictionary of summary statistics
    """
    stats = {}
    
    # Overall sales and profit metrics
    stats['total_sales'] = df['Sales'].sum()
    stats['total_profit'] = df['Profit Per Order'].sum()
    stats['average_profit_margin'] = df['Profit Margin'].mean()
    
    # Product metrics
    if 'Category Name' in df.columns:
        category_sales = df.groupby('Category Name')['Sales'].sum().sort_values(ascending=False)
        stats['top_selling_categories'] = category_sales.head(5).to_dict()
        
        category_profit = df.groupby('Category Name')['Profit Per Order'].sum().sort_values(ascending=False)
        stats['most_profitable_categories'] = category_profit.head(5).to_dict()
    
    # Geographic metrics
    if 'Customer Country' in df.columns:
        country_sales = df.groupby('Customer Country')['Sales'].sum().sort_values(ascending=False)
        stats['top_countries_by_sales'] = country_sales.head(5).to_dict()
    
    # Customer segment analysis
    if 'Customer Segment' in df.columns:
        segment_sales = df.groupby('Customer Segment')['Sales'].sum().sort_values(ascending=False)
        stats['segment_sales'] = segment_sales.to_dict()
        
        segment_profit = df.groupby('Customer Segment')['Profit Per Order'].sum().sort_values(ascending=False)
        stats['segment_profit'] = segment_profit.to_dict()
    
    return stats

def time_series_analysis(df):
    """
    Perform time series analysis on sales and profit data
    
    Parameters:
    df (pandas.DataFrame): Input data frame with datetime column 'Order Date'
    
    Returns:
    dict: Dictionary with time series data
    """
    time_series = {}
    
    # Check if necessary columns exist and are of right type
    if 'Order Date' not in df.columns or not pd.api.types.is_datetime64_any_dtype(df['Order Date']):
        return {'error': 'Order Date column missing or not in datetime format'}
    
    # Monthly sales and profit
    monthly_data = df.groupby(pd.Grouper(key='Order Date', freq='M')).agg({
        'Sales': 'sum',
        'Profit Per Order': 'sum',
        'Order Quantity': 'sum'
    }).reset_index()
    
    time_series['monthly'] = {
        'dates': monthly_data['Order Date'].dt.strftime('%Y-%m').tolist(),
        'sales': monthly_data['Sales'].tolist(),
        'profit': monthly_data['Profit Per Order'].tolist(),
        'quantity': monthly_data['Order Quantity'].tolist()
    }
    
    # Quarterly sales and profit
    quarterly_data = df.groupby(pd.Grouper(key='Order Date', freq='Q')).agg({
        'Sales': 'sum',
        'Profit Per Order': 'sum',
        'Order Quantity': 'sum'
    }).reset_index()
    
    time_series['quarterly'] = {
        'dates': quarterly_data['Order Date'].dt.strftime('%Y-Q%q').tolist(),
        'sales': quarterly_data['Sales'].tolist(),
        'profit': quarterly_data['Profit Per Order'].tolist(),
        'quantity': quarterly_data['Order Quantity'].tolist()
    }
    
    return time_series

def product_performance_analysis(df):
    """
    Analyze product performance based on sales, profit, and margin
    
    Parameters:
    df (pandas.DataFrame): Input data frame
    
    Returns:
    pandas.DataFrame: Product performance analysis
    """
    if 'Category Name' not in df.columns:
        return pd.DataFrame()
    
    # Group by product category
    product_perf = df.groupby('Category Name').agg({
        'Sales': 'sum',
        'Profit Per Order': 'sum',
        'Order Quantity': 'sum',
        'Profit Margin': 'mean'
    }).reset_index()
    
    # Calculate additional metrics
    product_perf['Average Sale Value'] = product_perf['Sales'] / product_perf['Order Quantity']
    product_perf['Profit per Unit'] = product_perf['Profit Per Order'] / product_perf['Order Quantity']
    
    # Sort by total sales descending
    product_perf = product_perf.sort_values('Sales', ascending=False)
    
    return product_perf
