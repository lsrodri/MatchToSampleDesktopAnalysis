import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Set font type for PDF export
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# Read the data
df = pd.read_csv('combined_results.csv')

# Filter for only V, VH, and H conditions
df = df[df['Condition'].isin(['V', 'VH', 'H'])]

# Replace boolean correctness values with 0 and 1
mapping = {False: 1, True: 0}
df['Correctness'] = df['Correctness'].map(mapping)

# Group by Participant ID, Condition, and Rendering and calculate means
df_grouped = df.groupby(['Participant ID', 'Condition', 'Rendering']).agg({'Correctness': 'mean', 'Reaction Time': 'mean'}).reset_index()

# Rename the 'Reaction Time' column to 'Reaction_Time'
df_grouped = df_grouped.rename(columns={'Reaction Time': 'Reaction_Time'})

# ----------------- Two-way ANOVA for Correctness -----------------

# Perform two-way ANOVA with interaction term for Correctness
model_correctness = ols('Correctness ~ C(Condition) * C(Rendering)', data=df_grouped).fit()
anova_correctness = sm.stats.anova_lm(model_correctness, typ=2)

# Print ANOVA table for Correctness
print("ANOVA for Correctness:")
print(anova_correctness)

# Perform Coefficients analysis for Correctness
coef_summary_correctness = model_correctness.summary()

# Print Coefficients analysis for Correctness
print("\nCoefficients for Correctness:")
print(coef_summary_correctness)

# ----------------- Two-way ANOVA for Response Time -----------------

# Perform two-way ANOVA with interaction term for Response Time
model_rt = ols('Reaction_Time ~ C(Condition) * C(Rendering)', data=df_grouped).fit()
anova_rt = sm.stats.anova_lm(model_rt, typ=2)

# Print ANOVA table for Response Time
print("\nANOVA for Response Time:")
print(anova_rt)

# Perform Coefficients analysis for Response Time
coef_summary_rt = model_rt.summary()

# Print Coefficients analysis for Response Time
print("\nCoefficients for Response Time:")
print(coef_summary_rt)

# ----------------- Graphs for Response Time and Correctness -----------------

# Create a new column that combines 'Rendering' and 'Condition'
df_grouped['Rendering_Condition'] = df_grouped['Rendering'] + ' ' + df_grouped['Condition']

# Sort the data so that the conditions are grouped together for each rendering
df_grouped = df_grouped.sort_values('Rendering_Condition')

# Define function to add significance bars
def add_significance_bar(ax, x1, x2, y, text):
    ax.plot([x1, x1, x2, x2], [y, y + 0.015, y + 0.015, y], lw=1.5, color='black')
    ax.text((x1 + x2) * .5, y + 0.015, text, ha='center', va='bottom', color='black')

# Create a single graph for Correctness
fig, ax = plt.subplots(figsize=(12, 6))

sns.boxplot(x="Rendering_Condition", y="Correctness", data=df_grouped, palette="colorblind", ax=ax)

# Perform and annotate t-tests for Desktop Rendering conditions
desktop_conditions = ['V', 'H', 'VH']
for i, cond1 in enumerate(desktop_conditions):
    for j, cond2 in enumerate(desktop_conditions):
        if i < j:
            group1 = df[(df['Rendering'] == 'Desktop') & (df['Condition'] == cond1)]['Correctness']
            group2 = df[(df['Rendering'] == 'Desktop') & (df['Condition'] == cond2)]['Correctness']
            t_stat, p_val = ttest_ind(group1, group2)
            if p_val < 0.05:
                max_val = df_grouped['Correctness'].max()
                add_significance_bar(ax, i, j, max_val + 0.06 * (j-i), '*')

# Perform and annotate t-tests for VR Rendering conditions
vr_conditions = ['V', 'H', 'VH']
offset = len(desktop_conditions)
for i, cond1 in enumerate(vr_conditions):
    for j, cond2 in enumerate(vr_conditions):
        if i < j:
            group1 = df[(df['Rendering'] == 'VR') & (df['Condition'] == cond1)]['Correctness']
            group2 = df[(df['Rendering'] == 'VR') & (df['Condition'] == cond2)]['Correctness']
            t_stat, p_val = ttest_ind(group1, group2)
            if p_val < 0.05:
                max_val = df_grouped['Correctness'].max()
                add_significance_bar(ax, offset + i, offset + j, max_val + 0.06 * (j-i), '*')

plt.title('Error Rates by Display Environment and Sensory Modality')
plt.xlabel('Display Environment and Sensory Modality')
plt.ylabel('Error Rate')

# Modify the x-axis labels
labels = ['Haptic (Surface)', 'Visual (Surface)', 'Visuohaptic (Surface)', 'Haptic (VR)', 'Visual (VR)', 'Visuohaptic (VR)']
ax.set_xticklabels(labels)

# plt.ylim(-0.5, 0.8)

plt.tight_layout()
plt.savefig('joint_error_rate.pdf', format='pdf')

# plt.show()

# Create a single graph for Reaction Time
fig, ax = plt.subplots(figsize=(12, 6))

sns.boxplot(x="Rendering_Condition", y="Reaction_Time", data=df_grouped, palette="colorblind", ax=ax)

# Perform and annotate t-tests for Desktop Rendering conditions (Reaction Time)
for i, cond1 in enumerate(desktop_conditions):
    for j, cond2 in enumerate(desktop_conditions):
        if i < j:
            group1 = df[(df['Rendering'] == 'Desktop') & (df['Condition'] == cond1)]['Reaction Time']
            group2 = df[(df['Rendering'] == 'Desktop') & (df['Condition'] == cond2)]['Reaction Time']
            t_stat, p_val = ttest_ind(group1, group2)
            if p_val < 0.05:
                x1, x2, x3 = 0, 1, 2
                y, h, col = df_grouped['Reaction_Time'].max() + 2, 2, 'k'
                
                plt.plot([x1, x1, x2, x2], [y-1.25, y-1, y-1, y-1.25], lw=1.5, c=col)
                plt.text((x1+x2)*.5, y-1, "*", ha='center', va='bottom', color=col)

                plt.plot([x1, x1, x3, x3], [y, y+0.25, y+0.25, y], lw=1.5, c=col)
                plt.text((x1+x3)*.5, y+0.25, "*", ha='center', va='bottom', color=col)

# Perform and annotate t-tests for VR Rendering conditions (Reaction Time)
for i, cond1 in enumerate(vr_conditions):
    for j, cond2 in enumerate(vr_conditions):
        if i < j:
            group1 = df[(df['Rendering'] == 'VR') & (df['Condition'] == cond1)]['Reaction Time']
            group2 = df[(df['Rendering'] == 'VR') & (df['Condition'] == cond2)]['Reaction Time']
            t_stat, p_val = ttest_ind(group1, group2)
            if p_val < 0.05:
                x1, x2, x3 = 3, 4, 5
                y, h, col = df_grouped['Reaction_Time'].max() + 2, 2, 'k'
                
                plt.plot([x1, x1, x2, x2], [y-1.25, y-1, y-1, y-1.25], lw=1.5, c=col)
                plt.text((x1+x2)*.5, y-1, "*", ha='center', va='bottom', color=col)

                plt.plot([x1, x1, x3, x3], [y, y+0.25, y+0.25, y], lw=1.5, c=col)
                plt.text((x1+x3)*.5, y+0.25, "*", ha='center', va='bottom', color=col)

plt.title('Response Time by Display Environment and Sensory Modality')
plt.xlabel('Display Environment and Sensory Modality')
plt.ylabel('Response Time in Seconds')

# Modify the x-axis labels
labels = ['Haptic (Surface)', 'Visual (Surface)', 'Visuohaptic (Surface)', 'Haptic (VR)', 'Visual (VR)', 'Visuohaptic (VR)']
ax.set_xticklabels(labels)

plt.tight_layout()
plt.savefig('joint_response_time.pdf', format='pdf')
plt.show()