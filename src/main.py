"""
Main script to run the entire Sales and Profit Performance Dashboard analysis pipeline.
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Add the src directory to Python path to import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing import load_data, clean_data, generate_features, save_processed_data
from src.analysis import calculate_summary_stats, time_series_analysis, product_performance_analysis
from src.visualization import (plot_sales_trend, plot_profit_margin_by_category, 
                             plot_sales_by_region, create_correlation_heatmap)

def main():
    """Main function to run the analysis pipeline"""
    
    # Define paths
    input_path = os.path.join('data', 'raw', 'Sales dataset.csv')
    processed_path = os.path.join('data', 'processed', 'sales_data_processed.csv')
    visualization_path = 'visualizations'
    
    print("Loading data...")
    df = load_data(input_path)
    print(f"Loaded {len(df)} records from {input_path}")
    
    print("\nCleaning data...")
    df_clean = clean_data(df)
    print(f"Data cleaned. {len(df_clean)} records remain after cleaning.")
    
    print("\nGenerating features...")
    df_enhanced = generate_features(df_clean)
    
    # Save processed data
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    save_processed_data(df_enhanced, processed_path)
    print(f"Processed data saved to {processed_path}")
    
    # Calculate summary statistics
    print("\nCalculating summary statistics...")
    summary_stats = calculate_summary_stats(df_enhanced)
    print(f"Total Sales: ${summary_stats['total_sales']:,.2f}")
    print(f"Total Profit: ${summary_stats['total_profit']:,.2f}")
    print(f"Average Profit Margin: {summary_stats['average_profit_margin']:.2%}")
    
    # Time series analysis
    print("\nPerforming time series analysis...")
    time_series = time_series_analysis(df_enhanced)
    
    # Product performance analysis
    print("\nAnalyzing product performance...")
    product_perf = product_performance_analysis(df_enhanced)
    print("Top 5 product categories by sales:")
    print(product_perf[['Category Name', 'Sales']].head(5))
    
    # Create visualizations
    print("\nCreating visualizations...")
    os.makedirs(visualization_path, exist_ok=True)
    
    # Sales trend visualization
    fig1 = plot_sales_trend(df_enhanced)
    if fig1:
        fig1.savefig(os.path.join(visualization_path, 'sales_trend.png'), 
                    dpi=300, bbox_inches='tight')
    
    # Profit margin by category visualization
    fig2 = plot_profit_margin_by_category(df_enhanced)
    if fig2:
        fig2.savefig(os.path.join(visualization_path, 'profit_margin_by_category.png'), 
                    dpi=300, bbox_inches='tight')
    
    # Sales by region visualization
    fig3 = plot_sales_by_region(df_enhanced)
    if fig3:
        fig3.savefig(os.path.join(visualization_path, 'sales_by_region.png'), 
                    dpi=300, bbox_inches='tight')
    
    # Correlation heatmap
    fig4 = create_correlation_heatmap(df_enhanced)
    if fig4:
        fig4.savefig(os.path.join(visualization_path, 'correlation_heatmap.png'), 
                    dpi=300, bbox_inches='tight')
    
    print("\nAnalysis complete. Visualizations saved to the 'visualizations' directory.")

if __name__ == "__main__":
    main()
