import pandas as pd
from scipy.stats import shapiro, f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Load data
data = pd.read_csv("combined_results.csv")

# Calculate Error column based on Correctness
data['Error'] = ~data['Correctness']

# Aggregate error rates per condition per participant
agg_data = data.groupby(['Rendering', 'Condition', 'Participant ID'])['Error'].mean().reset_index()

# Filter data for relevant columns
relevant_data = agg_data[['Rendering', 'Condition', 'Error']]

# Calculate error rates
error_rates = relevant_data.groupby(['Rendering', 'Condition']).mean()

# Calculate standard deviation, min, max
std_dev = relevant_data.groupby(['Rendering', 'Condition']).std()
min_values = relevant_data.groupby(['Rendering', 'Condition']).min()
max_values = relevant_data.groupby(['Rendering', 'Condition']).max()

# Shapiro-Wilk test for normality
shapiro_results = relevant_data.groupby(['Rendering', 'Condition']).apply(lambda x: shapiro(x['Error']))

# Repeated measures ANOVA
anova_results = f_oneway(*[relevant_data[relevant_data['Rendering'] == r]['Error'] for r in relevant_data['Rendering'].unique()])

# Post hoc tests
tukey_results = pairwise_tukeyhsd(relevant_data['Error'], relevant_data['Condition'])

print("Error Rates:")
print(error_rates)
print("\nStandard Deviation:")
print(std_dev)
print("\nMin Values:")
print(min_values)
print("\nMax Values:")
print(max_values)
print("\nShapiro-Wilk Test Results:")
print(shapiro_results)
print("\nANOVA Results:")
print("F-statistic:", anova_results.statistic)
print("p-value:", anova_results.pvalue)
print("\nPost Hoc Tukey Test Results:")
print(tukey_results)
