import pandas as pd
import matplotlib.pyplot as plt
import pingouin
from scipy.stats import mannwhitneyu
men_data = pd.read_csv('men_results.csv')
women_data = pd.read_csv('women_results.csv')
print(men_data.head())
print(women_data.head())
print(men_data.info())
print(women_data.info())
# Checking the frequency of each tournament type in both datasets
print(men_data['tournament'].value_counts())
print(women_data['tournament'].value_counts())
# Filtering for matches specifically from the FIFA World Cup in each dataset
FIFA_men_matches = men_data[men_data['tournament'] == 'FIFA World Cup']
FIFA_women_matches = women_data[women_data['tournament'] == 'FIFA World Cup']
# Further filtering to include only matches played after January 1, 2002
filtered_men_data = FIFA_men_matches[pd.to_datetime(FIFA_men_matches['date']) > '2002-01-01']
filtered_women_data = FIFA_women_matches[pd.to_datetime(FIFA_women_matches['date']) > '2002-01-01']
# Displaying the filtered data to verify the selections
print(filtered_men_data.head())
print(filtered_women_data.head())
# Adding a new column to each dataset indicating the group (men or women)
filtered_men_data['group'] = 'men'
filtered_women_data['group'] = 'women'
# Calculating total scores (home + away) for each match in both datasets
filtered_men_data['scores'] = filtered_men_data['home_score'] + filtered_men_data['away_score']
filtered_women_data['scores'] = filtered_women_data['home_score'] + filtered_women_data['away_score']
# Plotting a histogram of the scores for men’s matches
filtered_men_data['scores'].hist()
plt.show()
plt.clf()
filtered_women_data['scores'].hist()
plt.show()
plt.clf()
# Combining the filtered datasets (men and women) for comparison
comb = pd.concat([filtered_women_data, filtered_men_data], axis=0, ignore_index=True)
# Selecting relevant columns (scores and group) for the Mann-Whitney U test
data_subset = comb[['scores', 'group']]
data_subset_pivot = data_subset.pivot(columns='group', values='scores')  # Pivot data for analysis
# Performing the Mann-Whitney U test to compare scores between men’s and women’s matches
model = pingouin.mwu(x=data_subset_pivot['women'], y=data_subset_pivot['men'], alternative='greater')
# Extracting the p-value and determining the result based on a significance level of 0.01
p_val = model["p-val"].values[0]
result = 'reject' if p_val <= 0.01 else 'fail to reject'
# Storing the p-value and test result in a dictionary and displaying it
result_dict = {"p_val": p_val, "result": result}
print(result_dict)
