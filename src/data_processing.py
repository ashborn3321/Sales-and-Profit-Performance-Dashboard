"""
Data processing utility functions for the Sales and Profit Performance Dashboard.
This module contains functions for cleaning, transforming, and preparing the sales data.
"""

import pandas as pd
import numpy as np

def load_data(file_path):
    """
    Load the sales dataset from CSV file
    
    Parameters:
    file_path (str): Path to the CSV file
    
    Returns:
    pandas.DataFrame: Loaded data
    """
    return pd.read_csv(file_path)

def clean_data(df):
    """
    Clean the sales dataset by handling missing values, fixing data types, etc.
    
    Parameters:
    df (pandas.DataFrame): Input data frame
    
    Returns:
    pandas.DataFrame: Cleaned data frame
    """
    # Make a copy to avoid modifying the original data
    cleaned_df = df.copy()
    
    # Convert date columns to datetime
    if 'Order Date' in cleaned_df.columns:
        cleaned_df['Order Date'] = pd.to_datetime(cleaned_df['Order Date'], format='%d-%m-%Y', errors='coerce')
    
    # Remove rows with missing critical values (if any)
    cleaned_df = cleaned_df.dropna(subset=['Sales', 'Profit Margin', 'Profit Per Order'])
    
    # Convert numeric columns to proper numeric types
    numeric_cols = ['Sales', 'Profit Margin', 'Profit Per Order', 'Order Quantity', 'Product Price']
    for col in numeric_cols:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
    
    # Convert percentage strings to actual percentage values (if needed)
    if 'Profit Margin' in cleaned_df.columns and cleaned_df['Profit Margin'].dtype == 'object':
        cleaned_df['Profit Margin'] = cleaned_df['Profit Margin'].str.rstrip('%').astype(float) / 100
    
    return cleaned_df

def generate_features(df):
    """
    Generate new features from the existing data
    
    Parameters:
    df (pandas.DataFrame): Input data frame
    
    Returns:
    pandas.DataFrame: Data frame with new features
    """
    # Make a copy to avoid modifying the original data
    enhanced_df = df.copy()
    
    # Extract date components
    if 'Order Date' in enhanced_df.columns and pd.api.types.is_datetime64_any_dtype(enhanced_df['Order Date']):
        enhanced_df['Year'] = enhanced_df['Order Date'].dt.year
        enhanced_df['Month'] = enhanced_df['Order Date'].dt.month
        enhanced_df['Quarter'] = enhanced_df['Order Date'].dt.quarter
    
    # Calculate additional metrics
    if all(col in enhanced_df.columns for col in ['Sales', 'Profit Per Order']):
        # Profit ratio (different from margin)
        enhanced_df['Profit Ratio'] = enhanced_df['Profit Per Order'] / enhanced_df['Sales']
        
    return enhanced_df

def save_processed_data(df, output_path):
    """
    Save the processed data to CSV
    
    Parameters:
    df (pandas.DataFrame): Processed data frame
    output_path (str): Path where to save the processed CSV
    """
    df.to_csv(output_path, index=False)
