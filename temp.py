import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pingouin as pg

# Read the data
df = pd.read_csv('combined_results.csv')

# Convert 'Correctness' to binary values if needed
mapping = {False: 1, True: 0}
df['Correctness'] = df['Correctness'].map(mapping)

# Group by 'Participant ID', 'Condition', and 'Rendering' and calculate means
df_grouped = df.groupby(['Participant ID', 'Condition', 'Rendering']).agg({'Correctness': 'mean', 'Reaction Time': 'mean'}).reset_index()

# Visualization
sns.boxplot(x='Condition', y='Correctness', hue='Rendering', data=df_grouped)
plt.title('Error Rates by Condition and Rendering')
plt.xlabel('Condition')
plt.ylabel('Error Rate')
plt.show()

# Pairwise tests for interaction effect
pg.pairwise_ttests(data=df_grouped, dv='Correctness', between='Condition', within='Rendering', subject='Participant ID')