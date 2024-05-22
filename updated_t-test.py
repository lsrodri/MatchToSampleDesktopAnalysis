import pandas as pd
from scipy.stats import ttest_ind

# Load the combined data
df = pd.read_csv('results.csv')

# Calculate error rates and add a new column
df['Error Rate'] = 1 - df['Correctness']

# Calculate descriptive statistics for error rates and reaction time for each condition
error_rate_stats = df.groupby('Condition')['Error Rate'].mean()
reaction_time_stats = df.groupby('Condition')['Reaction Time'].mean()
reaction_time_std = df.groupby('Condition')['Reaction Time'].std()

print("Error Rate by Condition:")
for condition, mean_error_rate in error_rate_stats.items():
    print(f"{condition}: {mean_error_rate:.2f}")

print("\nReaction Time by Condition:")
for condition, mean_reaction_time in reaction_time_stats.items():
    print(f"{condition}: {mean_reaction_time:.2f}")

print("\nStandard Deviation of Reaction Time by Condition:")
for condition, std_reaction_time in reaction_time_std.items():
    print(f"{condition}: {std_reaction_time:.2f}")

# Report the number of unique participant ids in each condition
unique_participants = df.groupby('Condition')['Participant ID'].nunique()
print("\nNumber of Unique Participants by Condition:")
for condition, num_unique_participants in unique_participants.items():
    print(f"{condition}: {num_unique_participants}")

# Perform a t-test to determine if there are significant differences between conditions
conditions = df['Condition'].unique()

for i in range(len(conditions)):
    for j in range(i+1, len(conditions)):
        cond_i = df[df['Condition'] == conditions[i]]
        cond_j = df[df['Condition'] == conditions[j]]
        
        # For error rate
        t_stat, p_val = ttest_ind(cond_i['Error Rate'], cond_j['Error Rate'])
        print(f"\nT-test for error rate between {conditions[i]} and {conditions[j]}:")
        print(f"T-statistic: {t_stat:.2f}, p-value: {p_val:.2f}")

        # For reaction time
        t_stat, p_val = ttest_ind(cond_i['Reaction Time'], cond_j['Reaction Time'])
        print(f"\nT-test for reaction time between {conditions[i]} and {conditions[j]}:")
        print(f"T-statistic: {t_stat:.2f}, p-value: {p_val:.2f}")

# Calculate the mean error rate for each participant within each condition
participant_mean_error_rate = df.groupby(['Participant ID', 'Condition'])['Error Rate'].mean().reset_index()

# Calculate descriptive statistics for error rate and reaction time for each condition
error_rate_stats = participant_mean_error_rate.groupby('Condition')['Error Rate'].agg(['mean', 'std', 'count'])
reaction_time_stats = df.groupby('Condition')['Reaction Time'].agg(['mean', 'std', 'count'])

# Print mean error rate for each condition
print("Error Rate by Condition, aggregated per participant/condition mean:")
print(error_rate_stats)

# Print mean and std reaction time for each condition
print("Reaction Time by Condition, aggregated per participant/condition mean:")
print(reaction_time_stats)

# Perform a t-test to determine if there are significant differences between conditions for error rate
conditions = df['Condition'].unique()

for i in range(len(conditions)):
    for j in range(i + 1, len(conditions)):
        cond_i = participant_mean_error_rate[participant_mean_error_rate['Condition'] == conditions[i]]['Error Rate']
        cond_j = participant_mean_error_rate[participant_mean_error_rate['Condition'] == conditions[j]]['Error Rate']

        # For error rate
        t_stat, p_val = ttest_ind(cond_i, cond_j)
        print(f"\nT-test for error rate between {conditions[i]} and {conditions[j]}:")
        print(f"T-statistic: {t_stat:.2f}, p-value: {p_val:.2f}")

# Perform a t-test to determine if there are significant differences between conditions for reaction time
for i in range(len(conditions)):
    for j in range(i + 1, len(conditions)):
        cond_i = df[df['Condition'] == conditions[i]]['Reaction Time']
        cond_j = df[df['Condition'] == conditions[j]]['Reaction Time']

        # For reaction time
        t_stat, p_val = ttest_ind(cond_i, cond_j)
        print(f"\nT-test for reaction time between {conditions[i]} and {conditions[j]}:")
        print(f"T-statistic: {t_stat:.2f}, p-value: {p_val:.2f}")



# # Plot bar graphs with error bars for Correctness
# plt.figure(figsize=(10, 6))
# sns.barplot(x='Condition', y='mean', data=correctness_stats.reset_index(), yerr=correctness_stats['std'].values)
# plt.title("Correctness by Condition")
# plt.xlabel("Condition")
# plt.ylabel("Mean Correctness")
# plt.xticks(rotation=45)
# plt.show()

# # Plot bar graphs with error bars for Reaction Time
# plt.figure(figsize=(10, 6))
# sns.barplot(x='Condition', y='mean', data=reaction_time_stats.reset_index(), yerr=reaction_time_stats['std'].values)
# plt.title("Reaction Time by Condition")
# plt.xlabel("Condition")
# plt.ylabel("Mean Reaction Time")
# plt.xticks(rotation=45)
# plt.show()

# # Create strip plot with individual data points for Correctness
# plt.figure(figsize=(10, 6))
# sns.barplot(x='Condition', y='mean', data=correctness_stats.reset_index(), yerr=correctness_stats['std'].values)
# sns.stripplot(x='Condition', y='Correctness', data=participant_mean_correctness, jitter=True, color='black', alpha=0.5)
# plt.title("Correctness by Condition with Individual Data Points")
# plt.xlabel("Condition")
# plt.ylabel("Mean Correctness")
# plt.xticks(rotation=45)
# plt.show()

# # Create violin plots for Correctness
# plt.figure(figsize=(10, 6))
# sns.violinplot(x='Condition', y='Correctness', data=participant_mean_correctness, inner='stick', palette='Set2')
# plt.title("Correctness by Condition with Violin Plot")
# plt.xlabel("Condition")
# plt.ylabel("Mean Correctness")
# plt.xticks(rotation=45)
# plt.show()
