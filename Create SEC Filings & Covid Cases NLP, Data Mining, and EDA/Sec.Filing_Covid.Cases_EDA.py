#!/usr/bin/env python
# coding: utf-8

# ### BAIT 508 HW1: SEC Filings + COVID-19 Analytics
# 
# # DUE DATE: Monday, Nov 30th, 2020 11:59 p.m.!
# 
# 
# # Starter file

# - Before taking this assignment, please take a look at the instruction carefully.
# - In this assignment, you will use your Python skills (`pandas`, `matplotlib`, `for` loop, `if` condition, ...) to analyze SEC filings and Covid-19 cases.
# - There are short-answer questions and visualization questions. 
# - 20 problems, 5 points each, total 100 points
# - For visualization questions, save them separately using the specified file name: `hw1_ans(question_number)_(student_id).png` <br/>
# (e.g.) <b>hw1_ans13_37510930.png</b>
# - Please <b>don’t</b> submit the `png` file in Canvas. We will run your code to generate this `png` file!
# - Submit your Python code in UBC Canvas. DO NOT email your homework to instructors. 
# - Again, please submit your code in Canvas. The code file name should be as follows: `hw1_(student_id).py` <br/>
# (e.g.) <b>hw1_37510930.py</b>
# - If you are using Jupyter notebook, you can convert ipynb file to py file using the following procedure. <br/>
#   Click <b>File</b> tab -> Click <b>Download as</b> ->  Click <b>.py</b> option
# - If you do not keep the standard submission format, there will be an <b>extra deduction</b> on your grade. 
# - If code is not running, you will get <b>minimum</b> grade (Please run by yourself before submitting the assignment).
# - Late submissions will not be accepted!

# ### Import the appropriate modules for this assignment

# In[64]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


# ### Please assign the variables `first_name`, `last_name`, `student_id`, and `email` with your first name, last name, student ID, and email address. `student_id` should be an integer and others should be strings.

# In[65]:


first_name = "Zhao"
last_name = "Zhang"
student_id = 99007577
email = "jz7.zhao.zhang@gmail.com"


# ## [SEC analytics : Questions 1 - 13]

# ##### Question 1: Find the number of characters in this file and assign it to the `ans1` variable.
# - Download `feed_header_2017-2019.tsv` file into the same directory, where `hw1_starter.ipynb` is located. (If the code reads TSV file from another directory, there will be an extra deduction on your grade)
# - Use `open` function to open this `feed_header_2017-2019.tsv` file with `read-only` file mode. `TSV` file is similar to `CSV`, but its value is separated by `Tab`.
# 
# [Hint]
# - `open` function : https://www.w3schools.com/python/ref_func_open.asp

# In[66]:


# read the tsv file with read-only mode and assign it as file
file = open('feed_header_2017-2019.tsv',mode= 'r')
# assign tsv and finding the number of characters with len function
tsv = file.read()
ans1 = len(tsv)


# In[67]:


ans1


# ##### Question 2: Find the number of words in the file and assign it to the `ans2` variable.
# - We consider <b>word</b> as all numbers, special characters, and text separated by white space.

# In[68]:


# use split() to create a list of all words in the tsv file separated by white space
words = tsv.split()
ans2 = len(words)


# In[69]:


ans2


# ##### Question 3: Find the number of lines in the file and assign it to the `ans3` variable.

# In[70]:


# use split('\n') to seperate the tsv file by line, and loop the file to get the line counter
counter = 0
lines = tsv.split('\n')
for line in lines:
    if line:
        counter += 1
ans3 = counter


# In[71]:


ans3


# ### From now on, you will focus on one industry area for the industry trend analysis. 
# ### To do so, you will select the first digit `SIC` code.
# 
# ##### Question 4: Divide your `student_id` by 8, and add 1 to the `remainder`. Assign its value to the `ans4` variable.
# 

# In[72]:


ans4 = student_id % 8 + 1


# In[73]:


ans4


# ### Now, you have the first digit of `SIC` that you will analyze.
# ### Please extract the rows of the following condition. 
# - Read the `feed_header_2017-2019.tsv` using `pandas` module's `read_csv()` function and save the dataframe name as `df`.
# - We need to filter rows with an `ASSIGNED-SIC` column value starting with the value of `ans4`.      
# - You can extract this condition using various methods such as  `for` loop, `pandas`, and `numpy`.
# 
# 
# ##### Question 5: Find the shape of `df` and assign it to the `ans5` variable.

# In[74]:


# read the .tsv file using pd.read_csv, seperate by tab
dfraw = pd.read_csv('feed_header_2017-2019.tsv',sep='\t')


# In[75]:


# filter the data frame with ASSIGNED-SIC value that starts with ans4 (which is 2), 
df = dfraw[dfraw['ASSIGNED-SIC'] >= 2000]
df = df[df['ASSIGNED-SIC'] < 3000]


# In[76]:


ans5 = df.shape


# In[77]:


ans5


# ### From questions 6 to 8, you will analyze the `CONFORMED-NAME` column value from the dataframe `df`.

# ##### Question 6: Find the most common `word` among company names and assign it to the `ans6`.
# 
# - We consider <b>word</b> as all numbers, special characters, and text separated by white space.
# - You will get the <b>word</b> using the string's `split()` method.
# - For Question 6, each <b>word</b> is case-sensitive.
# 
# [Hint]
# 
# - `split()` method : https://www.w3schools.com/python/ref_string_split.asp

# In[78]:


cn1 = df['CONFORMED-NAME'].str.split()


# In[79]:


# convert the splitted pandas.Series to a list
cn2 = cn1.tolist()


# In[80]:


# convert the nested list to a flat list
# Reference: https://thispointer.com/python-convert-list-of-lists-or-nested-list-to-flat-list/
flatList = [ ele for lis in cn2 for ele in lis] 


# In[81]:


# use counter.most_common to return the word with the most count
c = Counter(flatList)
c.most_common(1)


# In[82]:


ans6 = c.most_common(1)[0][0]
ans6


# Take a look at the the answer of `ans6`. Do you think the answer is a stop word? Stop words are generally the most common words in a language and may not be meaningful such as `the`, `a`, `of` and `or`. In the company names, the following words can be stop words (`inc`, `co`, `se`, `ltd`, ... ). Therefore, you want to delete the stop words to get more meaningful result.

# ##### Question 7: Find the most common word among company names after removing stopwords and assign it to the `ans7`.
# - Please <b>lowercase</b> the company name value.
# - We consider <b>word</b> as all numbers, special characters, and text separated by white space.
# - Filter the word if the word includes any items among the provided `stopwords` list.

# In[83]:


# lowercase the company name values
dfq7 = df.copy()
dfq7['CONFORMED-NAME'] = dfq7['CONFORMED-NAME'].str.lower()


# In[84]:


stopwords = ['inc','corp','co','ltd','de','llc','group','inc.','holdings,','&','group,','lp','holdings']


# In[85]:


q7a = dfq7['CONFORMED-NAME'].str.split()


# In[86]:


q7b = q7a.to_list()
q7b = [ ele for lis in q7b for ele in lis] 


# In[87]:


q7c = []
for i in q7b:
    if i not in stopwords:
        q7c.append(i)


# In[88]:


c1 = Counter(q7c)
c1a = c1.most_common(1)


# In[89]:


ans7 = c1a[0][0]


# In[90]:


ans7


# ##### Question 8: Find the longest company name and assign it to the `ans8`.
# 
# - You do not need to split the value to extract the company name. 
# - Here are company name examples : `Apple, inc.`, `Amazon, inc.`

# In[91]:


df888 = df['CONFORMED-NAME'].to_list()


# In[92]:


# Finding the longest string in a list
# Reference: https://www.kite.com/python/answers/how-to-find-the-longest-string-in-a-list-in-python#:~:text=Use%20max()%20to%20find,of%20all%20strings%20in%20a_list%20.
max(df888,key=len)


# In[93]:


ans8 = max(df888,key=len)
ans8


# ### Questions 9 ~ 12: You want to analyze the trend of  `STATE` where the companies submit the `10-K` report in `2018` or `2019` from the `df` dataframe.
# - The first step is to make the new column, `year`, which includes the year value from `FILING-DATE` column.
# - Please convert the `year` column datatype as `int`.
# - Next, filter the dataframe with two conditions: <b>1)</b> `Form-Type` is `10-K` and <b>2)</b> `Year` is `2018` or `2019`. Assign the filtered dataframe as `df_10K`.

# ##### Question 9: Please find the unique number of states from the dataframe `df_10K` and assign it to the `ans9`.
# [Hint]
# - `.nunique()` method:  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.nunique.html

# In[94]:


# Slicing str value to get the first four digit of the Date section, which will be the year number
# Reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.slice.html
df['year'] = df['FILING-DATE'].str.slice(stop=4)

# Convert year value to integer 
df['year'] = df['year'].astype(int)


# In[95]:


# Next, filter the dataframe with two conditions: 
# 1) Form-Type is 10-K and 2) Year is 2018 or 2019. Assign the filtered dataframe as df_10K
df_10K = df[df['FORM-TYPE'] == '10-K']
df_10K = df_10K[ (df_10K['year'] == 2018) | (df_10K['year'] == 2019)]

# use nunique() to return the number of unique states from df_10K and assign it to ans9
ans9 = df_10K['STATE'].nunique()
ans9


# You are provided `states` information in `us_states.csv`. If comparing `states` list from  `df_10K`  with `us_states.csv`, you will notice that some state names are not in the valid 50 states. Therefore, you need to preprocess the `State` value in `df_10K` dataframe. 
# 
# Download `us_state.csv` file into the same directory, where `hw1_starter.ipynb` is located. (If your code reads `us_state.csv` file in another directory, there will be an extra deduction on your grade). Read the `us_states.csv` file and remove rows with invalid states from `df_10K` dataframe.
# 
# ##### Question 10: Please find the unique number of valid states from the dataframe `df_10K_state` and assign its value to the `ans10`.
# - Use the `pandas` library to open the `us_states.csv` file as a dataframe `usa_states`.
# - Get rid of rows which `STATE` column value is not the same as `State` column value from dataframe `usa_states`.
# - Save the preprocessed dataframe name as `df_10K_state`.
# - From `df_10K_state` dataframe, get the unique number of states and store it as `ans10`.

# In[96]:


# read us_states csv file and assign it to dataframe usa_states
usa_states = pd.read_csv('us_states.csv')
usa_states.head()


# In[97]:


# use .isin to find the states in df_10K that are contained in usa_states
# and filter out the states that is not in the usa_states, and assigned it to df_10K_state
df_10K_state = df_10K[df_10K['STATE'].isin(usa_states['State'])]

# find the unique number of states in df_10K_state
ans10 = df_10K_state['STATE'].nunique()
ans10


# #### Question 11: Find the states with the largest number of 10-K reports from dataframe `df_10K_state`, and assign this number to `ans11`.
# 
# [Hint]
# - To solve this question, you can refer the `Counter` object to check how many 10-K reporting is submitted by companies in each region.
# - `Counter` : https://docs.python.org/3/library/collections.html
# 

# In[98]:


# use counter to find the largest number of 10-K reports from df_10K_state
c11 = Counter(df_10K_state['STATE'])
c11.most_common(1)


# In[99]:


# assign the number of 10-K reports in the state with the largest number
ans11 = c11.most_common(1)[0][1]
ans11


# ##### Question 12: Find the number of `10-K` reports from the state of `NY` from the  `df_10K_state` dataframe.

# In[100]:


# use counter to find the number of reports in the state NY
c12 = Counter(df_10K_state['STATE'])
ans12 = c12['NY']
ans12


# ##### Question 13: Make the `bar` graph based on the following instructions.
# - You want to know the top <b>7</b> states where the `10-K` reports were most reported.
# - To make a <b>bar</b> graph, please use the `df_10K_state` dataframe.
# - Set all labels' font size as <b>15</b>. 
# - Set the xlabel as "`STATE`" (please use `state` column).
# - Set the ylabel as "`Number of 10-K reports`" (please use `STATE_COUNT` column value).
# - Set the title as "`Number of 10-K reports in 2018 and 2019`".
# - Save the graph named "`hw1_ans13_(student_id).png`".<br/>
#   (e.g.) <b>hw1_ans13_37510930.png</b>

# In[101]:


# find out the top 7 states w/ most reported 10-K forms
c12.most_common(7)
# for thought process clarity, create a c13 value same as c12.most_common(7)
c13 = c12.most_common(7)
# create a dictionary, update the dictionary key with state names and update the dictionary values with the number of 10-K forms
# Reference on updating dictionary https://www.w3schools.com/python/ref_dictionary_update.asp
q13dict = {}
for i in c13:
    q13dict.update({i[0]:i[1]})
q13dict


# In[102]:


# Plot the number of 10-K reports in 2018 and 2019 based on State and Number of 10-K reports
# Reference on bar chart plot using a dictionary
# https://www.kite.com/python/answers/how-to-plot-a-bar-chart-using-a-dictionary-in-matplotlib-in-python
# Saved Image could be cropped, so we use bbox_inches = 'tight' to avoid the situation
# Reference: https://stackoverflow.com/questions/37427362/plt-show-shows-full-graph-but-savefig-is-cropping-the-image/37428142
barx = q13dict.keys()
bary = q13dict.values()
plt.bar(barx,bary)
plt.xlabel('STATE',fontsize=15)
plt.ylabel('Number of 10-K reports',fontsize=15)
plt.title('Number of 10-K reports in 2018 and 2019',fontsize=15)
plt.savefig('hw1_ans13_99007577.png',bbox_inches='tight')
plt.show()


# You are now done with the SEC filings analytics part. Now we will move on to the next part.
# 
# ## [COVID-19 analytics : Questions 14 - 19]

# ### You want to calculate basic statistics and draw graphs on COVID-19 cases, which contain the information on `Reported_Date`, `HA`, `Sex`, and `Age_Group` from the `covid` dataframe.
# 
# - Download `BCCDC_COVID19_Dashboard_Case_Details.csv` file into the same directory, where `hw1_starter.ipynb` is located. (If your code reads CSV file from another directory, there will be an extra deduction on your grade)
# - Open `BCCDC_COVID19_Dashboard_Case_Details.csv` file using `pandas` library and assign the dataframe name as `covid`.

# ##### Question 14: Find how many COVID-19 cases occurred in October 2020 and assign its value to `ans14`. 
# 
# - The first step is to make the new column, `Month`, which includes month value from `Reported_Date` column.
# - Next, make the `list_Month` which contains the value of `Month` in `covid` dataframe.
# - Then, make the `month_count` dictionary which contains the month and the number of cases for that month.<br/>
#   (e.g.) <b>{'01': 1, '02': 8, ... }</b>
# - Finally, get the number of cases occured in October

# In[103]:


# read and store the BC-Covid csv file as covid
covid = pd.read_csv('BCCDC_COVID19_Dashboard_Case_Details.csv')


# In[104]:


# extract the month from the reported_date, which contains string values, with str.slice
# Reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.slice.html
covid['Month'] = covid['Reported_Date'].str.slice(start=5,stop=7)


# In[105]:


# convert the Month column in the dataframe to a list
list_Month = covid['Month'].to_list()


# In[106]:


# convert to set to get unique values of the list
# Reference: https://www.geeksforgeeks.org/python-get-unique-values-list/
q14set = set(list_Month)
q14list = list(q14set)
# sort the so the month is in ascending order, for q15
q14list.sort()


# In[107]:


# loop through each of the unique values of months and get the counts of that month in the list_Month
# map each unique value & their count as a key:value pair to the dictionary month_count
month_count = {}
for i in q14list: 
    month_count.update({i:list_Month.count(i)})


# In[108]:


# get the number of cases occurred in October (as represented by the key '10')
ans14 = month_count['10']
ans14


# ##### Question 15: Make the `bar` chart based on the following instructions.
# - You want to draw the `bar` chart to find out the trend in covid-19 by month based on the `list_Month` and `month_count`in Question 14.
# - X axis is the month in `list_Month` and Y axis is the number of cases in `month_count`.
# - Set all labels' font size as <b>15</b>. 
# - Set the xlabel as "`Months`".
# - Set the ylabel as "`The Number of Cases`".
# - Set the title as "`The Number of Cases by Months`".
# - Save the graph named "`hw1_ans15_(student_id).png`".<br/>
#   (e.g.) <b>hw1_ans15_37510930.png</b>

# In[109]:


# Create a barchart of different months in the list_Month and the number of cases in each month, using the dictionary month_count
# Reference on bar chart plot using a dictionary
# https://www.kite.com/python/answers/how-to-plot-a-bar-chart-using-a-dictionary-in-matplotlib-in-python

q15x = month_count.keys()
q15y = month_count.values()
plt.bar(q15x,q15y)
plt.xlabel('Months',fontsize=15)
plt.ylabel('The Number of Cases',fontsize=15)
plt.title('The Number of Cases by Months',fontsize=15)
plt.savefig('hw1_ans15_99007577.png',bbox_inches='tight')
plt.show()


# ### Questions 16~17: Make the `Line` plot by `Sex` and `Month`.
# - We want to divide the number of cases by `Sex` in question 15.
# 
# ##### Question 16: Find the month in which the number of female(`F`) cases were least and assign it to `ans16`. 
# - Column `Sex` consists of `M`,`F`,and `U`.
# - Calculate the number of cases in each `Sex` by `Month` as in Question 14.
# 
# - The first step is to divide `covid` dataframe into three sub-dataframes according to `Sex` values.
# - Next, make the `Male_Month`, `Female_Month`, and `Unknown_Month` which contains the value of `Month` in three sub-dataframe.
# - Then, make the `Male_count`, `Female_count`, and `Unknown_count` dictionary which contains the month and the number of cases for that month.<br/>
#   (e.g.) <b>{'01': 1, '02': 8, ... } for each `Sex`</b>
# - Finally, get the month in which the number of female(`F`) cases were least.

# In[110]:


# make three sub-dataframes based on gender from the covid dataframe
Male_Month = covid[covid['Sex']=='M']
Female_Month = covid[covid['Sex']=='F']
Unknown_Month = covid[covid['Sex']=='U']


# In[111]:


# convert the months value of the three sub-dataframes to a list
mml = Male_Month['Month'].to_list()
fml = Female_Month['Month'].to_list()
uml = Unknown_Month['Month'].to_list()

# convert to set to get unique values of the list
# Reference: https://www.geeksforgeeks.org/python-get-unique-values-list/
q16setm = set(mml)
q16setf = set(fml)
q16setu = set(uml)

# convert back have unique values in three lists
q16listm = list(q16setm)
q16listf = list(q16setf)
q16listu = list(q16setu)

# Sort the list so the data is in ascending order
q16listm.sort()
q16listf.sort()
q16listu.sort()

# loop through each of hte unique values of months and get the counts of that month in the list_Month
# map each unique value & their count as a key:value pair to the dictionary q16dict
Male_count = {}
for i in q16listm: 
    Male_count.update({i:mml.count(i)})

Female_count = {}
for i in q16listf: 
    Female_count.update({i:fml.count(i)})

Unknown_count = {}
for i in q16listu: 
    Unknown_count.update({i:uml.count(i)})


# In[112]:


# examine the Female_count to double-check ans16 answer
Female_count


# In[113]:


# find the month with the least number of cases in the female_count dictionary
ans16 = min(Female_count)
ans16


# ##### Question 17: Make the `line` plot based on the following instructions.
# - You want to distinguish the number of cases by `Month` between `Sex` to check whether there is different trend between `Sex`.
# - Draw the `plot` based on the `Male_Month`,`Female_Month`,`Unknown_Month`,`Male_count`,`Female_count`, and `Unknown_count`in Question 16.
# - Set all labels' font size as <b>15</b>. 
# - Set the xlabel as "`Months`" (please use `month_count` column values).
# - Set the ylabel as "`The Number of Cases by Sex`".
# - Set the title as "`The Number of Cases by Sex and Months`".
# - Save the graph named "`hw1_ans17_(student_id).png`".<br/>
#   (e.g.) <b>hw1_ans17_37510930.png</b>

# In[114]:


# create two lists for line plot, Mx for x-axis with months in male_count and My for y-axis with number of cases corresponding to the month
# do the same for each sex
Mx= list(Male_count.keys())
My = list(Male_count.values())

Fx= list(Female_count.keys())
Fy = list(Female_count.values())

Ux= list(Unknown_count.keys())
Uy = list(Unknown_count.values())


# In[115]:


# create a line plot with three lines each representing a sex
plt.plot(Mx,My,label='Male')
plt.plot(Fx,Fy,label='Female')
plt.plot(Ux,Uy,label='Unknown')
plt.xlabel('Months',fontsize=15)
plt.ylabel('The Number of Cases by Sex',fontsize=15)
plt.title('The Number of Cases by Sex and Months',fontsize=15)
plt.legend()
plt.savefig('hw1_ans17_99007577.png',bbox_inches='tight')
plt.show()


# ### Question 18~19: Make the `Horizontal bar` plot.
# 
# - B.C. began to be affected by the COVID-19 after mid-March.
# - Accordingly, we would like to check how many cases were reported in which region in <b>Question 18</b>.
# - Also, we would like to check the most reported area in <b>Question 19</b>. 
# - Select the code to aggregate `covid` dataframe by `HA` and `Month` and assign this dataframe as `covid_region`. 
# - In the dataframe `covid_region`, the columns that you need are `HA`, `Month`, and `Classification_Reported`.
# - Next, you need to make new column `Reported_cum`, which is the cumulative number of `Classification_Reported` of each `HA`.
# 
# [Hints]
# - `groupby(sum)` : https://stackoverflow.com/questions/39922986/pandas-group-by-and-sum
# - `cumsum` : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.cumsum.html
# - `lamda` : https://www.w3schools.com/python/python_lambda.asp

# In[116]:


# use groupby.count to get the number of cases reported in each month, grouped(indexed) by region and month
covid_region = covid.groupby(['HA','Month']).count()


# In[117]:


# extract and use the classification_reported column only
covid_region = covid_region[['Classification_Reported']]


# ##### Question 18: Draw the `Horizontal bar` graph when the `Month` is March(`03`).
# - Set all labels' font size as <b>15</b>. 
# - Set the xlabel as "`The Reported Number of Cases`"(Please use the value of `Classification_Reported`).
# - Set the ylabel as "`Region`".
# - Set the title as "`The Number of Cases in March`".
# - Save the graph named "`hw1_ans18_(student_id).png`".<br/>
#   (e.g.) <b>hw1_ans18_37510930.png</b>
# 
# [Hint]
# - `barh` : https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.barh.html

# In[118]:


# select rows based on multi-index value
# https://riptutorial.com/pandas/example/13285/select-from-multiindex-by-level
q18df = covid_region.loc[(covid_region.index.get_level_values('Month') == '03')]
q18df


# In[119]:


# reset index so we can easily access the region name and corresponding number of cases reported
q18df.reset_index(inplace=True)
q18df


# In[120]:


# create a horizontal bar plot based on instructions
# Reference: https://matplotlib.org/3.3.3/gallery/lines_bars_and_markers/barh.html
plt.barh(y=q18df['HA'], width=q18df['Classification_Reported'])
plt.xlabel('The Reported Number of Cases',fontsize=15)
plt.ylabel('Region',fontsize=15)
plt.title('Number of Cases in March',fontsize=15)
plt.savefig('hw1_ans18_99007577.png',bbox_inches='tight')
plt.show()


# ##### Question 19. Draw the `Horizontal bar` graph until the Month is August(08).
# - Assign different random colors and sort the region in descending order (in the number of cumulative cases).
# - Set all labels’ font size as <b>15</b>.
# - Set the xlabel as “`The Reported Culumative Number of Cases`” (Please use the value of `Reported_cum`).
# - Set the ylabel as “`Region`”.
# - Set the title as “`The Total Number of Cases Until August`”.
# - Save the graph named “`hw1_ans19_(student_id).png`”.<br/>
#  (e.g.) <b>hw1_ans19_37510930.png</b>
#  
# [Hint]
# - `random` : https://docs.python.org/3/library/random.html
# - `sort_values` : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
# - `map` : https://www.w3schools.com/python/ref_func_map.asp

# In[121]:


# use groupby.cumsum to get the cumulative number until each month by region
Reported_cum = covid_region.groupby(['HA']).cumsum()


# In[122]:


# select the rows with 'Month' at '08',or August, in each region
Reported_cum = Reported_cum.loc[(Reported_cum.index.get_level_values('Month') == '08')]
Reported_cum


# In[123]:


# reset index and sort_values by ascending order for the graph 
Reported_cum = Reported_cum.reset_index()
Reported_cum.sort_values(by='Classification_Reported',ascending=True,inplace=True)


# In[124]:


# Generating random color for matplot lib using RGB tuples with values between 0 and 1
# Reference https://www.kite.com/python/answers/how-to-generate-a-random-color-for-a-matplotlib-plot-in-python
# use numpy.random.rand(6,3) to generate 6 sets of 3 random numbers between 0 and 1, with each set representing a random color
# Reference: https://numpy.org/doc/stable/reference/random/generated/numpy.random.rand.html
# Reference: https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.rand.html
plt.barh(y=Reported_cum['HA'], width=Reported_cum['Classification_Reported'],color= np.random.rand(6,3))
plt.xlabel('The Reported Cumulative Number of Cases',fontsize=15)
plt.ylabel('Region',fontsize=15)
plt.title('The Toal Number of Cases Until March',fontsize=15)
plt.savefig('hw1_ans19_99007577.png',bbox_inches='tight')
plt.show()


# ##### Question 20: Make outfile name format as `hw1_answers_(student_id).txt` and save it to `txt` file                
# - when you write the answer, please keep format(please refer to word doc example).
# - You can save the result as txt file by using `open` function with `w` option.
# - file name should be like this : <b>hw1_answers_37510930.txt</b>

# In[125]:


outfile = open('hw1_answers_99007577.txt',mode='w')


# In[126]:


outfile.write('Zhang, Zhao, jz7.zhao.zhang@gmail.com')
outfile.write('\n answer1 = {} \n answer2 = {} \n answer3 = {}'.format(ans1,ans2,ans3))
outfile.write('\n answer4 = {} \n answer5 = {} \n answer6 = {}'.format(ans4,ans5,ans6))
outfile.write('\n answer7 = {} \n answer8 = {} \n answer9 = {}'.format(ans7,ans8,ans9))
outfile.write('\n answer10 = {} \n answer11 = {} \n answer12 = {}'.format(ans10,ans11,ans12))
outfile.write('\n answer14 = {} \n answer16 = {}'.format(ans14,ans16))
outfile.write('\n HW 1 is done!!!')
outfile.close()


# #### After finishing `hw1`, please submit your python code to Canvas. You don't need to submit the `.png` files. Also, don't submit the data files (`.tsv`, `.csv`) in Canvas. 
# 
# #### The code file name should be as follows: `hw1_(student_id).py` 
# (e.g.) hw1_37510930.py
