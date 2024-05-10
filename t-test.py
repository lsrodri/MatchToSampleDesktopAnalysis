import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns

# Load the combined data
df = pd.read_csv('results.csv')

# Remove the first two trials for each participant
# df = df[df.groupby('Participant ID')['Trial Number'].apply(lambda x: x > 2)]

# Calculate descriptive statistics for correctness and reaction time for each condition
correctness_stats = df.groupby('Condition')['Correctness'].mean()
reaction_time_stats = df.groupby('Condition')['Reaction Time'].mean()

print("Correctness by Condition:")
for condition, mean_correctness in correctness_stats.items():
    print(f"{condition}: {mean_correctness:.2f}")

print("\nReaction Time by Condition:")
for condition, mean_reaction_time in reaction_time_stats.items():
    print(f"{condition}: {mean_reaction_time:.2f}")

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
        
        # For correctness
        t_stat, p_val = ttest_ind(cond_i['Correctness'], cond_j['Correctness'])
        print(f"\nT-test for correctness between {conditions[i]} and {conditions[j]}:")
        print(f"T-statistic: {t_stat:.2f}, p-value: {p_val:.2f}")

        # For reaction time
        t_stat, p_val = ttest_ind(cond_i['Reaction Time'], cond_j['Reaction Time'])
        print(f"\nT-test for reaction time between {conditions[i]} and {conditions[j]}:")
        print(f"T-statistic: {t_stat:.2f}, p-value: {p_val:.2f}")


