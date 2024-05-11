import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('combined_results.csv')

# Prepare the data: map Correctness from True/False to 1/0
df['Correctness'] = df['Correctness'].astype(int)

# Calculate Error rate
df['Error_Rate'] = 1 - df['Correctness']

# Filter data for conditions V and VH only
df = df[df['Condition'].isin(['V', 'VH'])]

# Create interaction term
df['Condition_Rendering'] = df['Condition'] + '_' + df['Rendering']

# Fit logistic regression model with interaction term
model = smf.logit('Error_Rate ~ C(Condition) * C(Rendering)', data=df).fit()

# Print the summary of the model to see the p-values and coefficients
print(model.summary())

# Calculate predicted probabilities for each combination of Condition and Rendering
df['Predicted_Error_Rate'] = model.predict(df)

# Plot
sns.catplot(x='Condition', y='Predicted_Error_Rate', hue='Rendering', kind='bar', data=df)
plt.title('Predicted Error Rate by Condition and Rendering')
plt.ylabel('Predicted Probability of Error Rate')
plt.show()