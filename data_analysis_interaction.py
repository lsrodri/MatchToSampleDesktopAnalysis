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

# Filter for only V and VH conditions
df = df[df['Condition'].isin(['V', 'VH'])]

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

# ----------------- Interaction Plot -----------------

# Create an interaction plot for Correctness
sns.catplot(x='Condition', y='Correctness', hue='Rendering', kind='point', data=df_grouped, ci=None)

# Set plot labels and title
# plt.title('Interaction Plot of Condition and Rendering on Correctness')
plt.xlabel('Modality')
plt.ylabel('Error Rate')

# Show the plot
# plt.show()

# Create an interaction plot for Correctness
sns.catplot(x='Condition', y='Reaction_Time', hue='Rendering', kind='point', data=df_grouped, ci=None)

# Set plot labels and title
# plt.title('Interaction Plot of Condition and Rendering on Correctness')
plt.xlabel('Modality')
plt.ylabel('Error Rate')

# Show the plot
# plt.show()

# ----------------- Graphs for Response Time and Correctness -----------------

# Create a new column that combines 'Rendering' and 'Condition'
df_grouped['Rendering_Condition'] = df_grouped['Rendering'] + ' ' + df_grouped['Condition']

# Sort the data so that the conditions are grouped together for each rendering
df_grouped = df_grouped.sort_values('Rendering_Condition')

# Create a single graph for Reaction Time
fig, ax = plt.subplots(figsize=(12, 6))

sns.boxplot(x="Rendering_Condition", y="Reaction_Time", data=df_grouped, palette="colorblind", ax=ax)

# Perform a t-test to check for significant difference
group1 = df[(df['Rendering'] == 'Desktop') & (df['Condition'] == 'V')]['Reaction Time']
group2 = df[(df['Rendering'] == 'Desktop') & (df['Condition'] == 'VH')]['Reaction Time']
t_stat, p_val = ttest_ind(group1, group2)

# Add a horizontal bar with an asterisk if the difference is significant
if p_val < 0.05:
    y_max = max(max(group1), max(group2))
    ax.annotate("", xy=(0, y_max), xycoords='data',
                xytext=(1, y_max), textcoords='data',
                arrowprops=dict(arrowstyle="-", ec='#aaaaaa',
                                connectionstyle="bar,fraction=0.2"))
    ax.text(0.5, y_max + abs(y_max*0.05), "*", ha='center', va='bottom', color='k')

plt.title('Response Time by Rendering and Modality')
plt.xlabel('Rendering and Modality')
plt.ylabel('Response Time in Seconds')

plt.tight_layout()
plt.savefig('response_time.pdf', format='pdf')
# plt.show()

# Create a single graph for Correctness
fig, ax = plt.subplots(figsize=(12, 6))

sns.boxplot(x="Rendering_Condition", y="Correctness", data=df_grouped, palette="colorblind", ax=ax)

# Perform a t-test to check for significant difference for Desktop Rendering
group1_desktop = df[(df['Rendering'] == 'Desktop') & (df['Condition'] == 'V')]['Correctness']
group2_desktop = df[(df['Rendering'] == 'Desktop') & (df['Condition'] == 'VH')]['Correctness']
t_stat_desktop, p_val_desktop = ttest_ind(group1_desktop, group2_desktop)

# Add a horizontal bar with an asterisk if the difference is significant for Desktop Rendering
if p_val_desktop < 0.05:
    print('Significant difference in error rates between Desktop Visual and Desktop Visuohaptic')
    y_max_desktop = max(max(group1_desktop), max(group2_desktop))
    # Set the maximum y value as the height of the bar for Desktop Rendering
    bar_height_desktop = ax.get_ylim()[1]
    # Manually adjust the annotation position based on data range
    annotation_position_desktop = max(group1_desktop.mean(), group2_desktop.mean()) + abs(max(group1_desktop.mean(), group2_desktop.mean()) * 0.05) + 0.16
    # If the annotation is too close to the top of the plot, adjust its position
    if annotation_position_desktop > 0.95 * bar_height_desktop:
        annotation_position_desktop = 0.9 * bar_height_desktop
    ax.annotate("", xy=(0, annotation_position_desktop), xycoords='data',
                xytext=(1, annotation_position_desktop), textcoords='data',
                arrowprops=dict(arrowstyle="-", ec='#aaaaaa',
                                connectionstyle="bar,fraction=0.2"))
    # Position the asterisk above the bar for Desktop Rendering
    ax.text(0.5, annotation_position_desktop, "*", ha='center', va='bottom', color='k')


# Perform a t-test to check for significant difference for VR Rendering
group1_vr = df[(df['Rendering'] == 'VR') & (df['Condition'] == 'V')]['Correctness']
group2_vr = df[(df['Rendering'] == 'VR') & (df['Condition'] == 'VH')]['Correctness']
t_stat_vr, p_val_vr = ttest_ind(group1_vr, group2_vr)

# Add a horizontal bar with an asterisk if the difference is significant for VR Rendering
if p_val_vr < 0.05:
    y_max_vr = max(max(group1_vr), max(group2_vr))
    # Set the maximum y value as the height of the bar for VR Rendering
    bar_height_vr = ax.get_ylim()[1]
    # Manually adjust the annotation position based on data range
    annotation_position_vr = max(group1_vr.mean(), group2_vr.mean()) + abs(max(group1_vr.mean(), group2_vr.mean()) * 0.05) + 0.225
    # If the annotation is too close to the top of the plot, adjust its position
    # if annotation_position_vr > 0.95 * bar_height_vr:
    #     annotation_position_vr = 0.9 * bar_height_vr
    ax.annotate("", xy=(2, annotation_position_vr), xycoords='data',
                xytext=(3, annotation_position_vr), textcoords='data',
                arrowprops=dict(arrowstyle="-", ec='#aaaaaa',
                                connectionstyle="bar,fraction=0.2"))
    # Position the asterisk above the bar for VR Rendering
    ax.text(2.5, annotation_position_vr, "*", ha='center', va='bottom', color='k')


ax.set_ylim(bottom=-0.05, top=bar_height_desktop * 1.2)

plt.title('Error Rates by Rendering and Modality')
plt.xlabel('Rendering and Modality')
plt.ylabel('Error Rate')

plt.tight_layout()
plt.savefig('num_errors.pdf', format='pdf')
plt.show()
