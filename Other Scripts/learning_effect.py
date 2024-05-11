import pandas as pd
from scipy.stats import f_oneway

# Read the CSV file into a DataFrame
data = pd.read_csv('results.csv')

# Calculate the block number for each trial
data['Block'] = (data['Trial Number'] - 1) // 15 + 1

# Calculate the average correctness for each participant and block
avg_correctness = data.groupby(['Participant ID', 'Block'])['Correctness'].mean().reset_index()

# Pivot the data to have each block as a column
pivoted_data = avg_correctness.pivot(index='Participant ID', columns='Block', values='Correctness')

# Calculate the average correctness for each block
block_averages = pivoted_data.mean()

# Perform ANOVA on the pivoted data
f_statistic, p_value = f_oneway(*[pivoted_data[block] for block in pivoted_data.columns])

# Print the results
print("Block Averages:")
print(block_averages)

print("\nANOVA Results:")
print("F-statistic:", f_statistic)
print("p-value:", p_value)

# Check for significance level (e.g., 0.05)
alpha = 0.05
if p_value < alpha:
    print("There is a significant difference between blocks indicating a learning effect.")
else:
    print("There is no significant difference between blocks.")
