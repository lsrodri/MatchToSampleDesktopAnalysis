import pandas as pd

# Load your data
df = pd.read_csv('results.csv')

# Group data by Participant ID and calculate mean and standard deviation for Correctness
participant_stats = df.groupby('Participant ID')['Correctness'].agg(['mean', 'std'])

# Define the threshold for identifying outliers (e.g., 3 standard deviations)
threshold = 3

# Identify outliers for each participant
outliers = {}
for participant_id, data in participant_stats.iterrows():
    mean, std = data['mean'], data['std']
    lower_threshold = mean - threshold * std
    upper_threshold = mean + threshold * std
    participant_data = df[df['Participant ID'] == participant_id]
    potential_outliers = participant_data[(participant_data['Correctness'] < lower_threshold) | (participant_data['Correctness'] > upper_threshold)]
    if not potential_outliers.empty:
        outliers[participant_id] = potential_outliers

# Print or analyze the identified outliers
for participant_id, potential_outliers in outliers.items():
    print(f"Participant {participant_id} has {len(potential_outliers)} potential outliers:")
    relevant_columns = ['Participant ID', 'Trial Number', 'Condition', 'Correctness', 'Reaction Time']
    print(potential_outliers[relevant_columns])
