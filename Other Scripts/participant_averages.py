import pandas as pd

# Load your data
df = pd.read_csv('results.csv')

# Convert 'Correctness' to boolean (if not already)
df['Correctness'] = df['Correctness'].astype(bool)

# Group data by Participant ID and Condition, calculate mean and count correctness
participant_condition_stats = df.groupby(['Participant ID', 'Condition'])['Correctness'].agg(['mean', 'sum']).unstack()

# Create a new DataFrame for the output
output_df = pd.DataFrame(columns=['Participant', 'H Mean', 'V Mean', 'VH Mean', 'H Count', 'V Count', 'VH Count', 'Total Count'])

# Populate the output DataFrame
for participant_id, row in participant_condition_stats.iterrows():
    h_mean = row[('mean', 'H')]
    v_mean = row[('mean', 'V')]
    vh_mean = row[('mean', 'VH')]
    h_count = row[('sum', 'H')].astype(int)
    v_count = row[('sum', 'V')].astype(int)
    vh_count = row[('sum', 'VH')].astype(int)
    total_count = h_count + v_count + vh_count
    
    output_df = output_df.append({
        'Participant': participant_id,
        'H Mean': h_mean,
        'V Mean': v_mean,
        'VH Mean': vh_mean,
        'H Count': h_count,
        'V Count': v_count,
        'VH Count': vh_count,
        'Total Count': total_count
    }, ignore_index=True)

# Save the output DataFrame to a CSV file (optional)
output_df.to_csv('output_grouped_by_participant.csv', index=False)

# Display the output DataFrame
print(output_df)
