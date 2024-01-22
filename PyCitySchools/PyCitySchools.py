#!/usr/bin/env python
# coding: utf-8

# In[253]:


# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load (Remember to Change These)
school_data_to_load = Path("Resources/schools_complete.csv")
student_data_to_load = Path("Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# ## Local Government Area Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average maths score 
# 
# * Calculate the average reading score
# 
# * Calculate the percentage of students with a passing maths score (50 or greater)
# 
# * Calculate the percentage of students with a passing reading score (50 or greater)
# 
# * Calculate the percentage of students who passed maths **and** reading (% Overall Passing)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[254]:


#Calculate the total number of schools
school_count = len(school_data_complete["school_name"].unique())


#Calculate the total number of students
student_count = len(school_data_complete["Student ID"].unique())


#Calculate the total budget
total_budget = school_data["budget"].sum()
Formatted_total_budget = "${:,.2f}".format(total_budget)

#Calculate the average maths score
ave_maths_score = school_data_complete["maths_score"].mean()
ave_maths_score_str = f"{ave_maths_score:.6f}"

#Calculate the average reading score
ave_reading_score = school_data_complete["reading_score"].mean()
ave_reading_score_str = f"{ave_reading_score:.6f}"

#Calculate the percentage of students with a passing maths score (50 or greater)

passing_math_count = school_data_complete.loc[school_data_complete["maths_score"] >= 50,"maths_score"].count()
percentage_passing_math = (passing_math_count / student_count) * 100


# Calculate the percentage of students with a passing reading score (50 or greater)

passing_read_count = school_data_complete.loc[school_data_complete["reading_score"] >= 50,"reading_score"].count()
percentage_passing_read = (passing_read_count/student_count) * 100



#Calculate the percentage of students who passed maths and reading (% Overall Passing)
passing_both_count = len(school_data_complete[(school_data_complete["maths_score"] >= 50) 
                         & (school_data_complete["reading_score"] >= 50)])
Percentage_passing_both =(passing_both_count/student_count)* 100



# Create a dataframe to hold the above results

area_summary = pd.DataFrame({
    "Total No. of Schools": [school_count],
    "Total Students": [student_count],
    "Total Budget": [Formatted_total_budget],
    "Average Maths Score": [ave_maths_score_str],
    "Average Reading Score": [ave_reading_score_str],
    "% passing Maths": [percentage_passing_math],
    "% passing Reading": [percentage_passing_read],
    "% Overall Passing": [Percentage_passing_both]
})

# Display the DataFrame
area_summary


# ## School Summary

# * Create an overview table that summarises key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Maths Score
#   * Average Reading Score
#   * % Passing Maths
#   * % Passing Reading
#   * % Overall Passing (The percentage of students that passed maths **and** reading.)
#   
# * Create a dataframe to hold the above results

# In[255]:


# Group the data by school
grouped_school_data = school_data_complete.groupby('school_name')

# Calculating each metric
total_students = grouped_school_data.size()
total_budget = grouped_school_data['budget'].first()


per_student_budget = total_budget / total_students
average_math_score = grouped_school_data['maths_score'].mean()  
average_reading_score = grouped_school_data['reading_score'].mean()  
passing_math = school_data_complete[school_data_complete['maths_score'] >= 50].groupby('school_name').size()
passing_reading = school_data_complete[school_data_complete['reading_score'] >= 50].groupby('school_name').size()
passing_both = school_data_complete[(school_data_complete['maths_score'] >= 50) & (school_data_complete['reading_score'] >= 50)].groupby('school_name').size()

# Calculate percentages
percent_passing_math = (passing_math / total_students) * 100
percent_passing_reading = (passing_reading / total_students) * 100
percent_passing_both = (passing_both / total_students) * 100

# Create the DataFrame
per_school_summary = pd.DataFrame({
    "School Type": grouped_school_data['type'].first(), 
    "Total Students": total_students,
    "Total School Budget": total_budget,
    "Per Student Budget": per_student_budget,
    "Average Math Score": average_math_score,
    "Average Reading Score": average_reading_score,
    "% Passing Math": percent_passing_math,
    "% Passing Reading": percent_passing_reading,
    "% Overall Passing": percent_passing_both
})

# Display the DataFrame
per_school_summary


# ## Top Performing Schools (By % Overall Passing)

# * Sort and display the top five performing schools by % overall passing.

# In[256]:


top_five_schools = per_school_summary.sort_values('% Overall Passing', ascending=False).head(5)
top_five_schools


# ## Bottom Performing Schools (By % Overall Passing)

# * Sort and display the five worst-performing schools by % overall passing.

# In[257]:


top_five_schools = per_school_summary.sort_values('% Overall Passing', ascending=True).head(5)
top_five_schools


# ## Maths Scores by Year

# * Create a table that lists the average maths score for students of each year level (9, 10, 11, 12) at each school.
# 
#   * Create a pandas series for each year. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[258]:


# Create a series for each year level
year_9 = school_data_complete[school_data_complete['year'] == 9].groupby('school_name')['maths_score'].mean()
year_10 = school_data_complete[school_data_complete['year'] == 10].groupby('school_name')['maths_score'].mean()
year_11 = school_data_complete[school_data_complete['year'] == 11].groupby('school_name')['maths_score'].mean()
year_12 = school_data_complete[school_data_complete['year'] == 12].groupby('school_name')['maths_score'].mean()

# Combine the series into a DataFrame
math_scores_by_year = pd.DataFrame({
    'Year 9': year_9,
    'Year 10': year_10,
    'Year 11': year_11,
    'Year 12': year_12
})

# Optional: Formatting (e.g., rounding the scores to two decimal places)
math_scores_by_year = math_scores_by_year


# Display the DataFrame
math_scores_by_year


# ## Reading Score by Year

# * Perform the same operations as above for reading scores

# In[259]:


# Create a series for each year level
year_9 = school_data_complete[school_data_complete['year'] == 9].groupby('school_name')['reading_score'].mean()
year_10 = school_data_complete[school_data_complete['year'] == 10].groupby('school_name')['reading_score'].mean()
year_11 = school_data_complete[school_data_complete['year'] == 11].groupby('school_name')['reading_score'].mean()
year_12 = school_data_complete[school_data_complete['year'] == 12].groupby('school_name')['reading_score'].mean()

# Combine the series into a DataFrame
math_scores_by_year = pd.DataFrame({
    'Year 9': year_9,
    'Year 10': year_10,
    'Year 11': year_11,
    'Year 12': year_12
})

# Optional: Formatting (e.g., rounding the scores to two decimal places)
math_scores_by_year = math_scores_by_year


# Display the DataFrame
math_scores_by_year


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Maths Score
#   * Average Reading Score
#   * % Passing Maths
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[260]:


# Define spending bins and labels
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]

# Categorize spending based on the bins
per_school_summary["Spending Ranges (Per Student)"] = pd.cut(per_school_summary["Per Student Budget"], spending_bins, labels=labels)

# Calculate mean scores and passing rates per spending range
grouped_by_spending = per_school_summary.groupby(["Spending Ranges (Per Student)"], observed=True)

spending_math_scores = grouped_by_spending["Average Math Score"].mean()
spending_reading_scores = grouped_by_spending["Average Reading Score"].mean()
spending_passing_math = grouped_by_spending["% Passing Math"].mean()
spending_passing_reading = grouped_by_spending["% Passing Reading"].mean()
overall_passing_spending = grouped_by_spending["% Overall Passing"].mean()

ave_maths_score_formatted = spending_math_scores.map("{:.2f}".format)
ave_reading_score_formatted = spending_reading_scores.map("{:.2f}".format)
spending_passing_math_formatted = spending_passing_math.map("{:.2f}".format)
spending_passing_reading_formatted = spending_passing_reading.map("{:.2f}".format)
overall_passing_formatted = overall_passing_spending.map("{:.2f}".format)


# Create the spending_summary DataFrame
spending_summary = pd.DataFrame({
    "Average Math Score": ave_maths_score_formatted,
    "Average Reading Score": ave_reading_score_formatted,
    "% Passing Math": spending_passing_math_formatted,
    "% Passing Reading": spending_passing_reading_formatted,
    "% Overall Passing": overall_passing_formatted
})

# Display the spending_summary DataFrame
spending_summary



# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[261]:


# Define size bins and labels
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# Use pd.cut on the "Total Students" column
per_school_summary["School Size"] = pd.cut(per_school_summary["Total Students"], size_bins, labels=labels)

# Group by "School Size" and calculate averages for the required metrics
size_group = per_school_summary.groupby("School Size")

size_summary = pd.DataFrame({
    "Average Math Score": size_group["Average Math Score"].mean(),
    "Average Reading Score": size_group["Average Reading Score"].mean(),
    "% Passing Math": size_group["% Passing Math"].mean(),
    "% Passing Reading": size_group["% Passing Reading"].mean(),
    "% Overall Passing": size_group["% Overall Passing"].mean()
})

# Display the DataFrame
print(size_summary)


# ## Scores by School Type

# * Perform the same operations as above, based on school type

# In[263]:


# Assuming per_school_summary is already defined and has the necessary columns

# Group by "School Type" and calculate averages
type_group = per_school_summary.groupby("School Type")

# Create the type_summary DataFrame
type_summary = pd.DataFrame({
    "Average Math Score": type_group["Average Math Score"].mean(),
    "Average Reading Score": type_group["Average Reading Score"].mean(),
    "% Passing Math": type_group["% Passing Math"].mean(),
    "% Passing Reading": type_group["% Passing Reading"].mean(),
    "% Overall Passing": type_group["% Overall Passing"].mean()
})

# Display the DataFrame
print(type_summary)

