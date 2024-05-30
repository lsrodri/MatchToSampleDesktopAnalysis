import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import os

# Define the folder path
folder_path = 'NASA TLX'

# Construct the full file paths
vr_nasa_tlx_path = os.path.join(folder_path, 'VR_Nasa_TLX.csv')
desktop_nasa_tlx_path = os.path.join(folder_path, 'Desktop_Nasa_TLX.csv')

# Load the datasets
vr_nasa_tlx = pd.read_csv(vr_nasa_tlx_path)
desktop_nasa_tlx = pd.read_csv(desktop_nasa_tlx_path)

# Renaming the columns to a more manageable format
clean_column_names = {
    'Mental DemandHow mentally demanding was the task?  []': 'Mental Demand',
    'Physical DemandHow physically demanding was the task?  []': 'Physical Demand',
    'Temporal DemandHow hurried or rushed was the pace of the task?  []': 'Temporal Demand',
    'PerformanceHow successful were you in accomplishing what you were asked to do?  []': 'Performance',
    'EffortHow hard did you have to work to accomplish your level of performance?  []': 'Effort',
    'FrustrationHow insecure, discouraged, irritated, stressed, and annoyed were you? []': 'Frustration'
}

vr_nasa_tlx.rename(columns=clean_column_names, inplace=True)
desktop_nasa_tlx.rename(columns=clean_column_names, inplace=True)

# Ensure all relevant columns are numeric
columns_to_convert = ['Mental Demand', 'Physical Demand', 'Temporal Demand', 'Performance', 'Effort', 'Frustration']
vr_nasa_tlx[columns_to_convert] = vr_nasa_tlx[columns_to_convert].apply(pd.to_numeric, errors='coerce')
desktop_nasa_tlx[columns_to_convert] = desktop_nasa_tlx[columns_to_convert].apply(pd.to_numeric, errors='coerce')

# Filter out the specified participants
desktop_filtered = desktop_nasa_tlx[~desktop_nasa_tlx['Participant ID'].isin([10, 16])]
vr_filtered = vr_nasa_tlx[~vr_nasa_tlx['Participant ID'].isin([3, 16, 20])]

# Calculate new descriptive statistics
desktop_filtered_stats = desktop_filtered[columns_to_convert].describe()
vr_filtered_stats = vr_filtered[columns_to_convert].describe()

print("Desktop Filtered Statistics:\n", desktop_filtered_stats)
print("VR Filtered Statistics:\n", vr_filtered_stats)

# Conduct t-tests on the filtered data
filtered_t_test_results = {}

for column in columns_to_convert:
    t_stat, p_value = ttest_ind(vr_filtered[column].dropna(), desktop_filtered[column].dropna())
    filtered_t_test_results[column] = {'t-statistic': t_stat, 'p-value': p_value}

filtered_t_test_results_df = pd.DataFrame(filtered_t_test_results).T

print("\nFiltered T-Test Results:")
print(filtered_t_test_results_df)

# Calculate mean values for each dimension for both VR and Desktop in the filtered data
filtered_mean_values = {
    'VR': vr_filtered[columns_to_convert].mean(),
    'Desktop': desktop_filtered[columns_to_convert].mean()
}
filtered_mean_values_df = pd.DataFrame(filtered_mean_values)

# Calculate the standard deviation values for the filtered data
filtered_std_values = {
    'VR': vr_filtered[columns_to_convert].std(),
    'Desktop': desktop_filtered[columns_to_convert].std()
}
filtered_std_values_df = pd.DataFrame(filtered_std_values)

# Create bar graphs with error bars for standard deviation and significance annotations
fig, ax = plt.subplots(figsize=(14, 10))
filtered_mean_values_df.plot(kind='bar', yerr=filtered_std_values_df, capsize=4, ax=ax, color=['skyblue', 'salmon'])

# Add significance annotations
significant_threshold = 0.05
for i, dimension in enumerate(columns_to_convert):
    p_value = filtered_t_test_results_df.loc[dimension, 'p-value']
    if p_value < significant_threshold:
        # Get the coordinates of the bars
        bar_vr = ax.patches[i]
        bar_desktop = ax.patches[i + len(columns_to_convert)]
        
        # Calculate the position for the annotation
        x1 = bar_vr.get_x() + bar_vr.get_width() / 2
        x2 = bar_desktop.get_x() + bar_desktop.get_width() / 2
        y = max(bar_vr.get_height(), bar_desktop.get_height()) + 0.5
        
        # Add the annotation
        ax.text((x1 + x2) / 2, y + 0.25, '*', ha='center', va='bottom', color='black', fontsize=14)

ax.set_title('Mean NASA TLX Scores for VR and Desktop Conditions')
ax.set_xlabel('Dimensions')
ax.set_ylabel('Mean Scores')
plt.xticks(rotation=45)
plt.legend(title='Study', loc='upper right')

# Display the plot
plt.tight_layout()

# Save the figure as a PDF
plt.savefig('nasa_tlx_scores.pdf', format='pdf')

plt.show()
