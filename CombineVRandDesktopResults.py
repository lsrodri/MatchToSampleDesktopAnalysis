import pandas as pd
import glob
import os

# Define the folders to process
folders = ['VR', 'Desktop']

participantsPerGroup = 23

# Check if results.csv exists and delete it if it does
if os.path.exists('results.csv'):
    os.remove('results.csv')

# Process the csv files in each folder
for folder in folders:
    # Initialize an empty list to store the dataframes
    dfs = []

    # Get a list of all .csv files in the folder that do not contain '_probe' in the filename and is not 'Participants.csv'
    csv_files = [f for f in glob.glob(f'{folder}/*.csv') if '_probe' not in f and 'trials.csv' not in f]

    # Sort the files considering filenames as integers
    csv_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))

    # Read each file, strip leading/trailing spaces from column names, and concatenate them into one DataFrame
    for file in csv_files:
        df = pd.read_csv(file)
        df.rename(columns=lambda x: x.strip(), inplace=True)
        df['Rendering'] = folder  # Add the 'Rendering' column
        dfs.append(df)

    # Concatenate all the dataframes
    combined_df = pd.concat(dfs)

    # Convert the Start Timestamp and End Timestamp columns to datetime
    combined_df['Start Timestamp'] = pd.to_datetime(combined_df['Start Timestamp'])
    combined_df['End Timestamp'] = pd.to_datetime(combined_df['End Timestamp'])

    # Create a new column Reaction Time which is the difference of End Timestamp and Start Timestamp
    combined_df['Reaction Time'] = (combined_df['End Timestamp'] - combined_df['Start Timestamp']).dt.total_seconds()

    # Load the trials.csv into a DataFrame
    trials_df = pd.read_csv('trials.csv').rename(columns=lambda x: x.strip())  # strip spaces from this df too

    # Merge the combined_df and trials_df on "Participant ID" and "Trial Number"
    merge_columns = ['Participant ID', 'Trial Number']
    combined_df = pd.merge(combined_df, trials_df[merge_columns + ['Sample Number', 'Sample Order', 'Sample Time', 'Comparison Time', 'Condition', 'Path', 'Foil']],
                          on=merge_columns, how='left')

    # Sort the combined_df by "Participant ID", "Trial Number", and "End Timestamp" in descending order
    combined_df.sort_values(by=['Participant ID', 'Trial Number', 'End Timestamp'], ascending=[True, True, False], inplace=True)

    # Drop duplicates based on "Participant ID" and "Trial Number", keeping the first occurrence (latest row)
    combined_df.drop_duplicates(subset=['Participant ID', 'Trial Number'], keep='first', inplace=True)

    # In order to get unique Participant IDs for each group, add the number of participants per group to the Participant ID for the Desktop group
    if folder == 'Desktop':  # Check if the folder is 'Desktop'
            combined_df['Participant ID'] = combined_df['Participant ID'] + participantsPerGroup  

    # Append the combined DataFrame to the results.csv file
    if os.path.isfile('results.csv') and os.path.getsize('results.csv') > 0:
        # If the file exists and is not empty, write without header and leading newline
        combined_df.to_csv('results.csv', mode='a', header=False, index=False)
    else:
        # If the file does not exist or is empty, write with header
        combined_df.to_csv('results.csv', mode='a', header=True, index=False)