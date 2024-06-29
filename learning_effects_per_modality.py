import pandas as pd
from scipy.stats import kruskal, f_oneway, levene, shapiro
from statsmodels.formula.api import ols
import statsmodels.api as sm

# Load the combined dataset
combined_data = pd.read_csv('data.csv')

# Convert Correctness to numeric for analysis
combined_data['Correctness'] = combined_data['Correctness'].astype(int)

# Calculate the block number separately for each immersion type and modality
combined_data['Block'] = combined_data.groupby(['Immersion', 'Modality'])['TrialNumber'].transform(lambda x: (x - 1) // 15 + 1)

# Function to perform analysis for a given immersion type and modality
def analyze_modality(data, immersion_type, modality_type):
    data = data[(data['Immersion'] == immersion_type) & (data['Modality'] == modality_type)]
    
    # Correctness Analysis
    avg_correctness = data.groupby(['ParticipantID', 'Block'])['Correctness'].mean().reset_index()
    pivoted_data = avg_correctness.pivot(index='ParticipantID', columns='Block', values='Correctness')
    
    # ANOVA
    f_statistic, p_value = f_oneway(*[pivoted_data[block].dropna() for block in pivoted_data.columns])
    
    # Normality Test (Shapiro-Wilk)
    normality_results = {block: shapiro(pivoted_data[block].dropna()) for block in pivoted_data.columns}
    
    # Homogeneity of Variances Test (Levene's Test)
    levene_stat, levene_p = levene(*[pivoted_data[block].dropna() for block in pivoted_data.columns])
    
    # Kruskal-Wallis Test
    kruskal_stat, kruskal_p = kruskal(*[pivoted_data[block].dropna() for block in pivoted_data.columns])

    # Print Results
    print(f"\n{immersion_type} Study - {modality_type} Modality - Correctness:")
    print("Block Averages:")
    print(pivoted_data.mean())

    print("\nANOVA Results:")
    print("F-statistic:", f_statistic)
    print("p-value:", p_value)
    print("Significant difference between blocks." if p_value < 0.05 else "No significant difference between blocks.")

    print("\nNormality Test Results (Shapiro-Wilk):")
    for block, result in normality_results.items():
        print(f"Block {block}: W-statistic = {result.statistic}, p-value = {result.pvalue}")

    print("\nHomogeneity of Variances Test (Levene's Test):")
    print(f"Levene-statistic: {levene_stat}, p-value: {levene_p}")

    print("\nKruskal-Wallis Test:")
    print(f"Kruskal-statistic: {kruskal_stat}, p-value: {kruskal_p}")

# Analyze each modality for each immersion type
immersion_types = combined_data['Immersion'].unique()
modality_types = combined_data['Modality'].unique()

for immersion in immersion_types:
    for modality in modality_types:
        analyze_modality(combined_data, immersion, modality)
