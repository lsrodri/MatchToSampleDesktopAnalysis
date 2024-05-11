import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt
from scipy.stats import ttest_ind

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv('combined_results.csv')

# Filter for only V and VH conditions
df = df[df['Condition'].isin(['V', 'VH'])]

mapping = {False: 1, True: 0}
df = df.replace({'Correctness': mapping})

# Group by Rendering as well
df_rt = df.groupby(['Participant ID', 'Condition', 'Rendering'])[['Reaction Time']].mean()
df_err = df.groupby(['Participant ID', 'Condition', 'Rendering'])[['Correctness']].mean()

df_rt = df_rt.reset_index()
df_err = df_err.reset_index()

# Create a new column that combines 'Rendering' and 'Condition'
df_rt['Rendering_Condition'] = df_rt['Rendering'] + ' ' + df_rt['Condition']
df_err['Rendering_Condition'] = df_err['Rendering'] + ' ' + df_err['Condition']

# Sort the data so that the conditions are grouped together for each rendering
df_rt = df_rt.sort_values('Rendering_Condition')
df_err = df_err.sort_values('Rendering_Condition')

# Create a single graph for Reaction Time
fig, ax = plt.subplots(figsize=(12, 6))

g = sns.boxplot(x="Rendering_Condition", y="Reaction Time", data=df_rt, palette="colorblind", ax=ax)
g.set_xticks(range(4))
g.set_xticklabels(['Visual (Desktop)', 'Visuohaptic (Desktop)', 'Visual (VR)', 'Visuohaptic (VR)'])
g.set_ylabel('Response Time in Seconds')

# Perform a t-test to check for significant difference
group1 = df_rt[df_rt['Rendering_Condition'] == 'Desktop Visual']['Reaction Time']
group2 = df_rt[df_rt['Rendering_Condition'] == 'Desktop Visuohaptic']['Reaction Time']
t_stat, p_val = ttest_ind(group1, group2)

# Add a horizontal bar with an asterisk if the difference is significant
if p_val < 0.05:
    y_max = max(max(group1), max(group2))
    ax.annotate("", xy=(0, y_max), xycoords='data',
                xytext=(1, y_max), textcoords='data',
                arrowprops=dict(arrowstyle="-", ec='#aaaaaa',
                                connectionstyle="bar,fraction=0.2"))
    ax.text(0.5, y_max + abs(y_max*0.05), "*", ha='center', va='bottom', color='k')

plt.tight_layout()
plt.savefig('tct.pdf', format='pdf')
plt.show()

# Create a single graph for Correctness
fig, ax = plt.subplots(figsize=(12, 6))

g = sns.boxplot(x="Rendering_Condition", y="Correctness", data=df_err, palette="colorblind", ax=ax)
g.set_xticks(range(4))
g.set_xticklabels(['Visual (Desktop)', 'Visuohaptic (Desktop)', 'Visual (VR)', 'Visuohaptic (VR)'])
g.set_ylabel('Error Rate')

# Perform a t-test to check for significant difference
group1 = df_err[df_err['Rendering_Condition'] == 'Desktop Visual']['Correctness']
group2 = df_err[df_err['Rendering_Condition'] == 'Desktop Visuohaptic']['Correctness']
t_stat, p_val = ttest_ind(group1, group2)

# Add a horizontal bar with an asterisk if the difference is significant
if p_val < 0.05:
    y_max = max(max(group1), max(group2))
    ax.annotate("", xy=(0, y_max), xycoords='data',
                xytext=(1, y_max), textcoords='data',
                arrowprops=dict(arrowstyle="-", ec='#aaaaaa',
                                connectionstyle="bar,fraction=0.2"))
    ax.text(0.5, y_max + abs(y_max*0.05), "*", ha='center', va='bottom', color='k')

plt.tight_layout()
plt.savefig('num_errors.pdf', format='pdf')
plt.show()