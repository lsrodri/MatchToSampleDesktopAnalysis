import pandas as pd
from scipy.stats import kruskal, f_oneway, levene, shapiro
from statsmodels.formula.api import ols
import statsmodels.api as sm

# Load the combined dataset
combined_data = pd.read_csv('data.csv')

# Convert Correctness to numeric for analysis
combined_data['Correctness'] = combined_data['Correctness'].astype(int)

# Calculate the block number separately for each immersion type
combined_data['Block'] = combined_data.groupby('Immersion')['TrialNumber'].transform(lambda x: (x - 1) // 15 + 1)

# Function to perform analysis for a given immersion type
def analyze_immersion(data, immersion_type):
    data = data[data['Immersion'] == immersion_type]
    
    # Correctness Analysis
    avg_correctness = data.groupby(['ParticipantID', 'Block'])['Correctness'].mean().reset_index()
    pivoted_data = avg_correctness.pivot(index='ParticipantID', columns='Block', values='Correctness')
    f_statistic, p_value = f_oneway(*[pivoted_data[block].dropna() for block in pivoted_data.columns])
    normality_results = {block: shapiro(pivoted_data[block].dropna()) for block in pivoted_data.columns}
    levene_stat, levene_p = levene(*[pivoted_data[block].dropna() for block in pivoted_data.columns])
    kruskal_stat, kruskal_p = kruskal(*[pivoted_data[block].dropna() for block in pivoted_data.columns])

    print(f"\n{immersion_type} Study - Correctness:")
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

    print("\nKruskal-Wallis Test Results:")
    print("Kruskal-Wallis statistic:", kruskal_stat)
    print("p-value:", kruskal_p)

    # Response Time Analysis
    avg_response_time = data.groupby(['ParticipantID', 'Block'])['ReactionTime'].mean().reset_index()
    pivoted_data_rt = avg_response_time.pivot(index='ParticipantID', columns='Block', values='ReactionTime')
    f_statistic_rt, p_value_rt = f_oneway(*[pivoted_data_rt[block].dropna() for block in pivoted_data_rt.columns])
    normality_results_rt = {block: shapiro(pivoted_data_rt[block].dropna()) for block in pivoted_data_rt.columns}
    levene_stat_rt, levene_p_rt = levene(*[pivoted_data_rt[block].dropna() for block in pivoted_data_rt.columns])
    kruskal_stat_rt, kruskal_p_rt = kruskal(*[pivoted_data_rt[block].dropna() for block in pivoted_data_rt.columns])

    print(f"\n{immersion_type} Study - Response Time:")
    print("Block Averages:")
    print(pivoted_data_rt.mean())

    print("\nANOVA Results:")
    print("F-statistic:", f_statistic_rt)
    print("p-value:", p_value_rt)
    print("Significant difference between blocks." if p_value_rt < 0.05 else "No significant difference between blocks.")

    print("\nNormality Test Results (Shapiro-Wilk):")
    for block, result in normality_results_rt.items():
        print(f"Block {block}: W-statistic = {result.statistic}, p-value = {result.pvalue}")

    print("\nHomogeneity of Variances Test (Levene's Test):")
    print(f"Levene-statistic: {levene_stat_rt}, p-value: {levene_p_rt}")

    print("\nKruskal-Wallis Test Results:")
    print("Kruskal-Wallis statistic:", kruskal_stat_rt)
    print("p-value:", kruskal_p_rt)

# Perform separate analysis
analyze_immersion(combined_data, 'VR')
analyze_immersion(combined_data, 'Desktop')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Convert Correctness to numeric for analysis
combined_data['Correctness'] = combined_data['Correctness'].astype(int)

# Calculate Error Rate as 1 - Correctness
combined_data['ErrorRate'] = 1 - combined_data['Correctness']

# Calculate the block number separately for each immersion type
combined_data['Block'] = combined_data.groupby('Immersion')['TrialNumber'].transform(lambda x: (x - 1) // 15 + 1)

# Create a PdfPages object to save the plots
with PdfPages('learning_effects_plots.pdf') as pdf:
    
    # Create a figure for side-by-side plots
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot for Error Rates
    sns.lineplot(data=combined_data, x='Block', y='ErrorRate', hue='Immersion', marker='o', ax=axes[0])
    axes[0].set_title('Error Rates Across Experimental Runs')
    axes[0].set_xlabel('Experimental Run')
    axes[0].set_ylabel('Error Rate')
    axes[0].legend(title='Immersion')

    # Plot for Response Time
    sns.lineplot(data=combined_data, x='Block', y='ReactionTime', hue='Immersion', marker='o', ax=axes[1])
    axes[1].set_title('Response Times Across Experimental Runs')
    axes[1].set_xlabel('Experimental Run')
    axes[1].set_ylabel('Response Time (s)')
    axes[1].legend(title='Immersion')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure with side-by-side plots
    pdf.savefig(fig)  # Save the current figure
    plt.close()

# Notify the user
print("The plots have been saved to 'learning_effects_plots.pdf'.")

