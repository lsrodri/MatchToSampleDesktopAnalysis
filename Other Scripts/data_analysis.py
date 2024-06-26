# -*- coding: utf-8 -*-
"""Data Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RgQo27DidiigYJaob9YWxkqzplwcqXBl
"""

import numpy as np
import pandas as pd
# from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv('results.csv')

df.head()

mapping = {False: 1, True: 0}
df = df.replace({'Correctness': mapping})

df_rt = df.groupby(['Participant ID', 'Condition'])[['Reaction Time']].mean()
df_err = df.groupby(['Participant ID', 'Condition'])[['Correctness']].mean()

df_err

df_rt = df_rt.reset_index()
df_rt.head()

df_rt.boxplot(column='Reaction Time', by='Condition')

df_rt.groupby('Condition').std()

import pingouin as pg
pg.normality(df_rt, dv='Reaction Time', group='Condition', method='shapiro', alpha=0.05)

pg.friedman(data=df_rt, dv='Reaction Time', within='Condition', subject='Participant ID', method='chisq')

pg.pairwise_tests(data=df_rt, dv='Reaction Time', between=None, within='Condition', subject='Participant ID', parametric=False, marginal=True, alpha=0.05, alternative='two-sided', padjust='bonf', effsize='cohen', correction='auto', nan_policy='listwise', return_desc=False, interaction=True, within_first=True)

g = sns.boxplot(x="Condition", y="Reaction Time", data=df_rt, palette="colorblind")

g.set_xticks([0, 1, 2])
g.set_xticklabels(['Haptic', 'Visual', 'Visuohaptic'])
g.set_ylabel('Response Time in Seconds')

# statistical annotation
x1, x2, x3 = 0, 1, 2
y, h, col = df_rt['Reaction Time'].max() + 2, 2, 'k'

plt.plot([x1, x1, x2, x2], [y-1.25, y-1, y-1, y-1.25], lw=1.5, c=col)
plt.text((x1+x2)*.5, y-1, "*", ha='center', va='bottom', color=col)

plt.plot([x1, x1, x3, x3], [y, y+0.25, y+0.25, y], lw=1.5, c=col)
plt.text((x1+x3)*.5, y+0.25, "*", ha='center', va='bottom', color=col)

plt.ylim(0, 19)
plt.yticks(ticks=plt.yticks()[0], labels=plt.yticks()[0].astype(int))

plt.tight_layout()
# plt.savefig('tct.pdf', format='pdf')

plt.show()

df_err = df_err.reset_index()
df_err.head()

df_err.boxplot(column='Correctness', by='Condition')

df_err.groupby('Condition').std()

import pingouin as pg
pg.normality(df_err, dv='Correctness', group='Condition', method='shapiro', alpha=0.05)

pg.rm_anova(data=df_err, dv='Correctness', within='Condition', subject='Participant ID', correction='auto', detailed=False, effsize='ng2')

pg.pairwise_tests(data=df_err, dv='Correctness', between=None, within='Condition', subject='Participant ID', parametric=True, marginal=True, alpha=0.05, alternative='two-sided', padjust='bonf', effsize='cohen', correction='auto', nan_policy='listwise', return_desc=False, interaction=True, within_first=True)

g = sns.boxplot(x="Condition", y="Correctness", data=df_err, palette="colorblind")

g.set_xticks([0, 1, 2])
g.set_xticklabels(['Haptic', 'Visual', 'Visuohaptic'])
g.set_ylabel('Error Rate')

# statistical annotation
x1, x2, x3 = 0, 1, 2
y, h, col = df_err['Correctness'].max() + 1.25, 2, 'k'

plt.plot([x1, x1, x2, x2], [0.5, 0.51, 0.51, 0.5], lw=1.5, c=col)
plt.text((x1+x2)*.5, 0.51, "*", ha='center', va='bottom', color=col)

plt.plot([x2, x2, x3, x3], [0.5, 0.51, 0.51, 0.5], lw=1.5, c=col)
plt.text((x2+x3)*.5, 0.51, "*", ha='center', va='bottom', color=col)

plt.plot([x1, x1, x3, x3], [0.54, 0.55, 0.55, 0.54], lw=1.5, c=col)
plt.text((x1+x3)*.5, 0.55, "*", ha='center', va='bottom', color=col)

plt.ylim(0, 0.7)

plt.tight_layout()
# plt.savefig('num_errors.pdf', format='pdf')

plt.show()

