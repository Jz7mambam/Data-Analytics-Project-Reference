#!/usr/bin/env python
# coding: utf-8

# ### BAIT 508 HW2: SEC Filings Text Analytics
# 
# # DUE DATE: Friday, Dec 6th, 2020 11:59 p.m.!
# # Starter file
# This assignment was developed by Jaecheol Park, Myunghwan Lee, and Gene Moo Lee.

# - <b>Before taking this assignment, please take a look at the instruction carefully.</b>
# - In this assignment, you will use your NLP and Python skills (`pandas`, `BeautifulSoup`, `nltk`, `wordcloud`, user-defined functions, ...) to analyze text data of SEC filings and answer the following questions.
# - There are short-answer questions and visualization questions. 
# - 20 problems, 5 points each, total 100 points
# - For visualization questions, save them separately using the specified file name: `hw2_ans(question_number)_(student_id).png` <br/>
# (e.g.) <b>hw2_ans13_37510930.png</b>
# - Please <b>don’t</b> submit the `png` file in Canvas. We will run your code to generate this `png` file!
# - Submit your Python code in UBC Canvas. DO NOT email your homework to instructors. 
# - Again, please submit your code in Canvas. The code file name should be as follows: `hw2_(student_id).py` <br/>
# (e.g.) <b>hw2_37510930.py</b>
# - If you do not keep the standard submission format, there will be an <b>extra deduction</b> on your grade. 
# - If code is not running, you will get <b>minimum</b> grade (Please run by yourself before submitting the assignment).
# - Late submissions will not be accepted!

# ### Import the appropriate libraries you need for this assignment.

# In[2]:


import json
import nltk
import string
import spacy
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
from collections import Counter
from wordcloud import WordCloud
from textblob import TextBlob
from nltk.tokenize import sent_tokenize, word_tokenize
from pprint import pprint
import csv
import time
import requests
from bs4 import BeautifulSoup
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Please assign the variables `first_name`, `last_name`, `student_id`, and `email` with your first name, last name, student ID, and email address.

# In[3]:


first_name = 'Zhao'
last_name = 'Zhang'
email = 'jz7.zhao.zhang@gmail.com'


# ## Download and preprocess the data
# 
# - Download `corpus_10k_2015-2019.csv` file into the same directory, where `hw2_starter.ipynb` is located. (If not, there will be an extra deduction on your grade)
# 
# - First, create user-defined `isYear` function with two parameters (`target_year`, `text`) which check the `year`column value is the same as `target_year` in the `text`.
# - Second, open `corpus_10k_2015-2019.csv` file with `open` function and filter the data which the `year` is `2019` from <b>the first 10,000 companies</b> using `isYear` function you defined.
# - Save the filtered data as a `txt` file called `corpus.subset.txt`.
# 
# [Hint]
# - `open` function : https://www.w3schools.com/python/ref_func_open.asp
# 

# In[4]:


# Create a isYear function that takes a integer year value and text, and return true if the 5th value of text is a string value that's the same as target_year
# becasue the csv file stores year value as str, hence str()
def isYear(target_year,text):
        if text[4] == str(target_year):
            return True
        else:
            return False


# In[5]:


infile = open('corpus_10k_2015-2019.csv',mode ='r')

outfile = open('corpus.subtext.txt',mode='w')

# take the first line of the infile (the header line, and manually write a headerline)
# Reference: https://www.kite.com/python/answers/how-to-read-the-first-and-last-line-of-a-file-in-python
outfile.write(infile.readline() +'\n')

# loop through the csv file splitted by line and seperated by comma, so each line in the file corresponds to a row in the csv
# write outfile(the filtered 'corpus.subtext.txt') line by line (row by row)
# use try: except: pass to bypass errors such as runtime error
# https://docs.python.org/3/tutorial/errors.html
loopfile = infile.read()
for line in loopfile.split('\n'):
    try:
        if isYear(2019,line.split(','))==True:
            outfile.write(line+'\n')       
    except:
        pass

#close both files
infile.close()    
outfile.close()


# - Create dataframe `df` from `corpus.subset.txt` that you made right before, and view the first 5 rows using `head` method.

# - Drop <b>the columns</b> where <b>all elements are `NaN`</b> (in other words, this column contains no useful information)
#  using `dropna()` method from `pandas`.
#  
# 
# [Hint]
# - `dropna()` method : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html

# In[6]:


# use pd.read_csv to read the filtered data file
df = pd.read_csv('corpus.subtext.txt')


# In[7]:


# drop entirely missing columns
df.dropna(how="all",axis=1,inplace=True)
# replace other missing values with empty string
df.fillna("",inplace=True)


# - Fill <b>the missing values</b> with <b>empty string ("")</b> using `fillna()` method from `pandas`.
# - Then, view the first 5 rows to confirm that missing values have been replaced using `head` method. 
# 
# [Hint]
# - `fillna()` method : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html

# In[8]:


# checking if shape is the same as mentioned in Piazza
df.shape


# ##  Scrape SIC code and names on the web using BeautifulSoup 
# - Collect the industry names for sic codes from the <b>"List"</b> section (not "Range") of the Wikipedia page (https://en.wikipedia.org/wiki/Standard_Industrial_Classification).
# - Create `code_to_industry_name` dictionary where the `key` is the sic code and the `value` is the industry name.
# - Then, replace the SIC code "0100 (01111...)" from the table with 0100.
# 

# In[9]:


# store wiki page in variable url
url = 'https://en.wikipedia.org/wiki/Standard_Industrial_Classification'
r = requests.get(url)


# In[10]:


# Extracts the response as html: html_doc
html_doc = r.text

# Create a BeautifulSoup object from the HTML: soup
soup = BeautifulSoup(html_doc, "lxml")


# In[11]:


pretty_soup = soup.prettify()


# In[12]:


# locate all the tables in the page
table_tags = soup.find_all('table', {'class': 'wikitable sortable'})


# In[13]:


industries = []
# There are two table tags in the page, we want the List table, hence table_tags[1]
# Create a industries list with all the content in the SIC code - Industry Name List table
for row in table_tags[1].find_all('tr'):
    for td in row.find_all('td'):
        industries.append(td.get_text().strip())


# In[14]:


# Store SIC code in the SICs list and Industry name in the INDs lsit
SICs = []
INDs = []
for i in range(len(industries)):
    if i % 2 == 0:
        SICs.append(industries[i])
    else: 
        INDs.append(industries[i])


# In[15]:


# Create empty dicitonary
code_to_industry_name = {}


# In[16]:


# update key:value pair based on SIC codes:Industry name
for i in range(len(SICs)):
    code_to_industry_name.update({SICs[i]:INDs[i]})        


# - Add a new column `industry_name` to `df` using `lambda` function. (You may use other approaches if needed)
# - Values in `industry_name` must correspond to the `sic` in the `df`.
# - For example, if a row has a SIC code of `1000`, then value of its industry name will be `Forestry`.
# 
# [Hint]
# - `lamda` : https://www.w3schools.com/python/python_lambda.asp

# In[17]:


# creating a column using a dictionary
# Reference: https://cmdlinetips.com/2018/01/how-to-add-a-new-column-to-using-a-dictionary-in-pandas-data-frame/
# .astype(str) - transform integer values in sic column to string values to correspond to key values in the dictionary
df['industry_name'] = df['sic'].astype(str).map(code_to_industry_name)


# ## Now, you get the preprocess dataframe `df` to analyze.
# 
# ## Industry analysis (Q1-Q4)
# ### Question1. What are the 5 most common industry names? Get them from `industry_name`, not from `sic` code
# - Store a list of 5 most common industry names in `ans1`.

# In[18]:


# show the 5 most common values in the industry_name column in a tuple
c1 = Counter(df['industry_name'])
c1.most_common(5)


# In[19]:


# create the answer list from tuple
ans1list = []
for i in range(len(c1.most_common(5))):
    ans1list.append(c1.most_common(5)[i][0])


# In[20]:


#assign ans1
ans1 = ans1list


# ### Question2. Out of all the industries with the prefix `Services`, what are the 4 most common industry names?
# - Store a list of 4 most common industry names in `ans2`.

# In[22]:


#service industry list
sil = df.loc[df['industry_name'].str.startswith('Services') == True,'industry_name']


# In[23]:


# find the most common 4 industry names with prefix Services
c2 = Counter(sil)
c2.most_common(4)


# In[24]:


# create accumulator list to transform tuple values to a list and extract the names of the industries
ans2list = []
for i in range(len(c2.most_common(4))):
    ans2list.append(c2.most_common(4)[i][0])


# In[25]:


# assign ans2
ans2 = ans2list


# ### Question3. What is the `name` of the company `id` with `1353611-2019`?
# - Store the company name as a string in `ans3`.

# In[27]:


# find the company name with id 1353611-2019
a3l = list(df.loc[df['id']=='1353611-2019','name'])


# In[28]:


# assign ans3
ans3 = a3l[0]


# ### Question4. What is the `industry_name` of the company with name `Solar Quartz Technologies Corp`?
# - Store the industry name as a string in `ans4`.

# In[30]:


# find the industry_name of the company named Solar Quartz Technologies Corp
ans4list = list(df.loc[df['name']=='Solar Quartz Technologies Corp','industry_name'])


# In[31]:


# assign ans4
ans4 = ans4list[0]


# ## Keyword analysis (Q5 and Q6)
# 
# ### For Q5 and Q6 you will filter out stopwords and non-alphanumeric English characters. 
# - You can use `nltk.corpus.stopwords` for our definition of stopwords. 
# - Alphanumeric English characters are letters in the alphabet (`a-z`) and numbers (`0-9`).
# - For example, <b>"Python is awesome :scream_cat:"</b> would be filtered to <b>"Python awesome"</b> after removing stopwords (in this case "is") and the emoji (non-alphanumeric).
# 
# [Hint]
# - `nltk.corpus` for stopwords : https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
# 

# In[33]:


# finding the english stopwords from the nltk module and assign it as stopwords
stopwords = nltk.corpus.stopwords.words('english')


# ### Question5. What are the 5 most common words from the `Item_5` column?
# - Store a list of the 5 most common words in `ans5`.

# In[34]:


# transform the pandas series into a list
ans5list = list(df['item_5'])


# In[35]:


# write a txt file to extract each element in the list
with open('Q5&6.text',mode='w') as q5file:
    for i in ans5list:
        q5file.write(i)


# In[36]:


# make it lowercase
with open('Q5&6.text',mode='r') as f:
    words = nltk.word_tokenize(f.read().lower())


# In[37]:


# count the words & finding out the 5 most common with their counts
c5 = Counter(words)
c5.most_common(5)


# In[38]:


# extract the words from the tuple and assign it to a list
ans5list = []
for i in range(len(c5.most_common(5))):
    ans5list.append(c5.most_common(5)[i][0])


# In[39]:


# assign ans5
ans5 = ans5list


# ### Question6. What are the 5 most common words from the `Item_5` column without stopwords?
# - Store a list of the 5 most common words in `ans6`.

# In[41]:


# our accumulator list
words2 = [] 
# filter non-alphanumeric characters with str.isalnum() and filter stopwords
# Reference: https://www.kite.com/python/answers/how-to-remove-all-non-alphanumeric-characters-from-a-string-in-python
for w in words:
    if w not in stopwords and w.isalnum()==True:
        words2.append(w)


# In[42]:


# count the words and find out 5 most common ones
c6 = Counter(words2)
c6.most_common(5)


# In[43]:


# extract values in the tuple and assign it to a list
ans6list = []
for i in range(len(c6.most_common(5))):
    ans6list.append(c6.most_common(5)[i][0])


# In[44]:


# assign ans6
ans6 = ans6list


# ## Named Entity Recognition (Q7-Q9)
# 
# - If any of the entities are spaces, exclude them in the analysis.
# - For example, `(" ")` is not a valid entity.

# In[46]:


# extract first 100 rows and save them as a list - same for the other questions below
ans7list = list(df['item_1'][0:100])
# use the list to create a txt file for nlp processing - same for other questions below
with open('Q7.txt',mode='w') as q7file:
    for i in ans7list:
        q7file.write(i)


# ### Question7. What are the 5 most common `PERSON` named entities overall from the `item_1` column?
# - Store a list of the 5 most common `PERSON` named entities in `ans7`.

# In[ ]:


with open('Q7.txt',mode='r') as f7:
     article = f7.read()


# In[ ]:


# download spacy and en_core_web_sm
get_ipython().system('python -m spacy download en_core_web_sm')


# In[ ]:


# load spacy and save as nlp
nlp = spacy.load('en_core_web_sm', tagger=False, parser=False, matcher=False)
nlp.max_length = 10000000


# In[ ]:


doc = nlp(article)


# In[ ]:


# create a PERSONs list of the text values labelled as PERSON in the spacy module
PERSONs = []
for ent in doc.ents:
    if ent.label_ == 'PERSON':
        PERSONs.append(ent.text)


# In[ ]:


# count the most common 5 values of the list
c7 = Counter(PERSONs)
c7.most_common(5)


# In[ ]:


# transer the tuple to a list and extract the names (ignore the count) - same for other codes below
ans7list = []
for i in range(len(c7.most_common(5))):
    ans7list.append(c7.most_common(5)[i][0])


# In[ ]:


# ans7 variable assignment
ans7 = ans7list


# ### Question8. What are the 5 most common `ORG` named entities overall from the `item_2` column? 
# - Store a list of the 5 most common `ORG` named entities in `ans8`.
# - ORG: Companies, agencies, institutions, etc.

# In[60]:


ans8list = list(df['item_2'][0:100])
with open('Q8.txt',mode='w') as q8file:
    for i in ans8list:
        q8file.write(i)


# In[61]:


with open('Q8.txt',mode='r') as f8:
     article8 = f8.read()


# In[62]:


doc8 = nlp(article8)


# In[63]:


# create a ORGs list of the text values labelled as ORG in the spacy module
ORGs = []
for ent in doc8.ents:
    if ent.label_ == 'ORG':
        ORGs.append(ent.text)


# In[64]:


# counting the values in the ORGs list & find out 5 most common ones
c8 = Counter(ORGs)
c8.most_common(5)


# In[65]:


# extract values in the tuple and assign it into a list
ans8list = []
for i in range(len(c8.most_common(5))):
    ans8list.append(c8.most_common(5)[i][0])


# In[66]:


# assign ans8
ans8 = ans8list
ans8


# ### Question9. What are the 4 most common named entities overall from the `item_9` column?
# - Store a list of the 4 most common named entities in `ans9`.

# In[67]:


ans9list = list(df['item_9'][0:100])
with open('Q9.txt',mode='w') as q9file:
    for i in ans9list:
        q9file.write(i)


# In[68]:


with open('Q9.txt',mode='r') as f9:
     article9 = f9.read()


# In[69]:


doc9 = nlp(article9)


# In[70]:


doc9ents = []
for ent in doc9.ents:
    doc9ents.append(ent.text)


# In[71]:


c9 = Counter(doc9ents)
c9.most_common(4)


# In[72]:


ans9list = []
for i in range(len(c9.most_common(4))):
    ans9list.append(c9.most_common(4)[i][0])


# In[73]:


ans9 = ans9list
ans9


# ## NER for specific firm (Q10-Q12)
# - You want to find the information on the company with id `1653710-2019`.
# - Given list comprehension, you want to find out common entities in the dataframe `df`.

# In[74]:


columns = [col for col in df.columns if 'item' in col]


# In[75]:


Q10df = df.loc[df['id']=='1653710-2019',columns]


# In[76]:


Q10df


# ### Question10. What are the 4 most common `PERSON` named entities mentioned by the company with id `1653710-2019` across all `item_*` rows/columns?
# - Store a list of the 4 most common `PERSON` named entities in `ans10`.

# In[77]:


# use for ele in columns inside iterrows to go over each value under each column and aggregate them to a list
Q10list = []
for label,row in Q10df.iterrows():
    for ele in columns:
        Q10list.append(Q10df.loc[label,ele])


# In[78]:


# write a txt file based on this list for nlp processing
with open('Q10.txt',mode='w') as q10file:
    for i in Q10list:
        q10file.write(i)


# In[79]:


with open('Q10.txt',mode='r') as f10:
     article10 = f10.read()


# In[80]:


doc10 = nlp(article10)
# find out the text values labeled as PERSON and store them in a list
doc10ents = []
for ent in doc10.ents:
    if ent.label_ == 'PERSON':
        doc10ents.append(ent.text)


# In[81]:


# count and extract 4 most common values, store it in ans10list
c10 = Counter(doc10ents)
ans10list = []
for i in range(len(c10.most_common(4))):
    ans10list.append(c10.most_common(4)[i][0])


# In[82]:


#assign ans10
ans10 = ans10list


# ### Question11. What are the 2 most common `GPE` named entities mentioned by the company with id `1653710-2019` across all `item_*` rows/columns?
# - Store a list of the 2 most common `GPE` named entities in `ans11`.

# In[84]:


# find out the text values labeled as GPE and store them in a list
doc11ents = []
for ent in doc10.ents:
    if ent.label_ == 'GPE':
        doc11ents.append(ent.text)


# In[85]:


# get the two most common text values in a list
c11 = Counter(doc11ents)
ans11list = []
for i in range(len(c11.most_common(2))):
    ans11list.append(c11.most_common(2)[i][0])


# In[86]:


ans11 = ans11list


# ### Question12. What are the 5 most common named entities mentioned by the company with id `1653710-2019` across all `item_*` rows/columns?
# - Store a list of the 5 most common named entities in `ans12`.

# In[87]:


# find out the text values of named entities and store them in a list
doc12ents = []
for ent in doc10.ents:
    doc12ents.append(ent.text)


# In[88]:


# get the five most common text values in a list
c12 = Counter(doc12ents)
ans12list = []
for i in range(len(c12.most_common(5))):
    ans12list.append(c12.most_common(5)[i][0])


# In[89]:


ans12 = ans12list


# ## Twitter analysis (Q13-Q15)
# ### `tweets.json` collected  50,000 tweets containing below keywords: 
# - Keyword : `analytics`, `technology`, `big data`, `machine learning`, `artificial intelligence`
# - The way used to collect the Twitter streaming data is using `tweepy` and `twython` module.
# - `tweepy` for Twitter streaming : http://docs.tweepy.org/en/latest/streaming_how_to.html
# 
# ### Save and read the `tweets.json` file as `tweets` 
# - Download `tweets.json` file into the same directory, where `hw2_starter.ipynb` is located. (If not, there will be an extra deduction on your grade)
# - Open `tweets.json` file as `tweets` with `open` function.
# 
# [Hint]
# - `open` function : https://www.w3schools.com/python/ref_func_open.asp

# In[48]:


# loading the tweets json file 
with open('tweets.json') as infile13:
    data = json.load(infile13)


# ### Question13. In the collected 50,000 tweets, what are the 100 most common words after removing stop words?
# - Store a list of the 100 most common words in `ans13`.

# In[49]:


# Codes below follows Gene's in-class notes 
# words13 is a list of lowercased text values in the json file
words13 = []
for i in range(len(data)):
    words13.append(data[i]['text'].lower())
# words14 is a nested list of individual words of each tweet
words14 = []
for i in words13:
    words14.append(i.split())
# words15 is a list of individual words of the 50000 tweets    
words15 = []
for i in range(len(words14)):
    for k in range(len(words14[i])):
        words15.append(words14[i][k])


# In[92]:


# list comprehension to remove stopwords and non-alphanumeric values from the word list
# Reference: https://www.programiz.com/python-programming/methods/string/isalnum
# Reference: https://www.kite.com/python/answers/how-to-remove-all-non-alphanumeric-characters-from-a-string-in-python
words16 = [w for w in words15 if w not in stopwords and w.isalnum()==True]


# In[93]:


# finding the most common 100 words after the filter, put them in a list, and assign to ans13 
c13 = Counter(words16)
ans13list = []
for i in range(len(c13.most_common(100))):
    ans13list.append(c13.most_common(100)[i][0])


# In[94]:


ans13 = ans13list


# ### Question14. Find the firm that has the most common words between `item_1` and 50,000 tweets. 
# - First, find the 100 most common words of each firm's `item_1` column.
# - Then, use the top the top 100 most common words of the 50,000 tweets after removing stop words (`ans13`) to find the most common words between `item_1` and 50,000 tweets. 
# - Disregard the word count, we are only interested in the number of unqiue words that appear in intersection of both common words.
# - Store the answer as a string in `ans14`.

# In[96]:


Q14list = list(df['item_1'][0:100])


# In[97]:


# Create a nested list of each company's individual words
Q14words = []
for item in Q14list:
    Q14words.append(item.lower().split())


# In[98]:


# Create a list of words filtered by stopwords and non-alphanumeric 
Q14words1 = []
for ele in Q14words:
    Q14words1.append(Counter(w for w in ele if w not in stopwords and w.isalnum()==True).most_common(100))


# In[99]:


# Create a unique counter list of the number of shared common words in both ans13 and each firm's item_1 column
uniquecounterlist = []
for ele in Q14words1:
    uniquecounter = 0
    for i in range(len(ele)):       
        if ele[i][0] in ans13list:
            uniquecounter += 1
    uniquecounterlist.append(uniquecounter)


# In[100]:


# return the index of the largest number of uniquecounterlist (largest number of shared common words)
q14index = uniquecounterlist.index(max(uniquecounterlist))


# In[101]:


# locate the name of the company in the dataframe
ans14 = df.loc[q14index,'name']


# ### Question15. In the collected 50,000 tweets, what are the 5 most common named entities mentioned?
# - You need to use the NER for this question.
# - Store a list of the 5 most common named entities in `ans15`.

# In[103]:


# form a list of the text of 50000 tweets
q15words = []
for i in range(len(data)):
    q15words.append(data[i-1]['text'])


# In[104]:


#remove empty strings
q15words = [i for i in q15words if i]


# In[105]:


# write the tweets text into a txt file
with open('Q15.txt',encoding='utf-8',mode='w') as q15file:
    for ele in q15words:
        q15file.write(ele)


# In[106]:


with open('Q15.txt',encoding='utf-8',mode='r') as f15:
     article15 = f15.read()


# In[107]:


doc15 = nlp(article15)


# In[108]:


# use nlp to find the 5 most common named entities mentioned in the tweets
doc15ents = []

for ent in doc15.ents:
    doc15ents.append(ent.text)

c15 = Counter(doc15ents)
ans15list = []

for i in range(len(c15.most_common(5))):
    ans15list.append(c15.most_common(5)[i][0])


# In[109]:


ans15 = ans15list


# ## For the following analyses, find the top two most common industries names
# - Assign the most common industry name as `top_1` and the second most common industry name as `top_2`.

# In[112]:


q16list = list(df['industry_name'])


# In[113]:


# return the two most common industry names
c16 = Counter(q16list)
c16.most_common(2)


# In[114]:


# variable assignment
top1 = c16.most_common(2)[0][0]
top2 = c16.most_common(2)[1][0]


# In[115]:


print(top1,top2)


# ## Word cloud and sentiment analysis (Q16-Q19)
# 
# - Use `wordcloud` library and `WordCloud` function in it.
# - Define user-defined `generate_wordcloud` function with one parameter `values` to generate word cloud for one input value.
# - You don't need `axis` in the wordcloud and use `bilinear` interpolation. 
# 
# [Hint]
# - `bilinear` for `imshow()` : https://matplotlib.org/3.3.1/gallery/images_contours_and_fields/interpolation_methods.html

# In[116]:


# top1 = 'Blank Checks'
# top2 = 'Pharmaceutical Preparations'


# In[149]:


def generate_wordcloud(values):
    wordcloud = WordCloud(width=800, height=400).generate(values)
    plt.figure(figsize=(20,10)) # set up figure size
    plt.imshow(wordcloud,interpolation='bilinear') # word cloud image show
    plt.axis("off") # turn on axis


# ### Question16. Make two separate wordclouds for `item_1` column.
# - One for the most common industry and another one for the second most common industry.
# - Save the graph named "`hw2_ans16a_(student_id).png`" and "`hw2_ans16b_(student_id).png`".<br/>
#   (e.g.) <b>hw2_ans16a_37510930.png</b>, <b>hw2_ans16b_37510930.png</b>, respectively.

# In[118]:


top1list = list(df.loc[df['industry_name']==top1,'item_1'])
top2list = list(df.loc[df['industry_name']==top2,'item_1'])


# In[119]:


# create two string accumulators that aggregate the values of each industry's item_1 content
top1string = ""
for item in top1list:
    top1string = top1string+ item + ' '


    
top2string = ""
for item in top2list:
    top2string = top2string+ item + ' '


# In[150]:


# generate wordcloud and save figure as per instructions
generate_wordcloud(top1string)
plt.savefig('hw2_ans16a_99007577.png')
plt.show()


# In[151]:


generate_wordcloud(top2string)
plt.savefig('hw2_ans16b_99007577.png')
plt.show()


# ### Question17. Make two separate wordclouds for `item_1a`column.
# - One for the most common industry and another one for the second most common industry.
# - Save the graph named "`hw2_ans17a_(student_id).png`" and "`hw2_ans17b_(student_id).png`".<br/>
#   (e.g.) <b>hw2_ans17a_37510930.png</b>, <b>hw2_ans17b_37510930.png</b>, respectively.

# In[122]:


top1q17 = list(df.loc[df['industry_name']==top1,'item_1a'])
top2q17 = list(df.loc[df['industry_name']==top2,'item_1a'])
# create two string accumulators that aggregate the values of each industry's item_1a content
q17string1 = ""
for item in top1q17:
    q17string1 = q17string1+ item + ' '

    
q17string2 = ""
for item in top2q17:
    q17string2 = q17string2+ item + ' '


# In[123]:


generate_wordcloud(q17string1)
plt.savefig('hw2_ans17a_99007577.png')
plt.show()


# In[152]:


generate_wordcloud(q17string2)
plt.savefig('hw2_ans17b_99007577.png')
plt.show()


# ### Question18. Make two separate wordclouds for `item_7` column
# - One for the most common industry and another one for the second most common industry.
# - Save the graph named "`hw2_ans18a_(student_id).png`" and "`hw2_ans18b_(student_id).png`".<br/>
#   (e.g.) <b>hw2_ans18a_37510930.png</b>, <b>hw2_ans18b_37510930.png</b>, respectively.

# In[125]:


top1q18 = list(df.loc[df['industry_name']==top1,'item_7'])
top2q18 = list(df.loc[df['industry_name']==top2,'item_7'])

# create two string accumulators that aggregate the values of each industry's item_7 content
q18string1 = ""
for item in top1q18:
    q18string1 = q18string1+ item + ' '

    
q18string2 = ""
for item in top2q18:
    q18string2 = q18string2+ item + ' '


# In[153]:


generate_wordcloud(q18string1)
plt.savefig('hw2_ans18a_99007577.png')
plt.show()


# In[154]:


generate_wordcloud(q18string2)
plt.savefig('hw2_ans18b_99007577.png')
plt.show()


# ### Question19. Make two histograms of the polarity for `item_1a` column. 
# - One for the most common industry and another one for the second most common industry.
# - Save the graph named "`hw2_ans19a_(student_id).png`" and "`hw2_ans19b_(student_id).png`".<br/>
#   (e.g.) <b>hw2_ans19a_37510930.png</b>, <b>hw2_ans19b_37510930.png</b>, respectively.

# In[128]:


top1q19 = list(df.loc[df['industry_name']==top1,'item_1a'])
top2q19 = list(df.loc[df['industry_name']==top2,'item_1a'])


# In[129]:


# Create a list containing the polarity score of each item1a in the top1 industry
pol_list1 = []
for ele in top1q19:
    tb = TextBlob(ele)
    pol_list1.append(tb.sentiment.polarity)

# Create a histogram with polarity score and count
plt.hist(pol_list1, bins=10)
plt.xlabel('Polarity Score')
plt.ylabel('Item Count')
plt.grid(True)
plt.savefig('hw2_ans19a_99007577.png')
plt.show()


# In[130]:


# Create a list containing the polarity score of each item1a in the top2 industry
pol_list2 = []
for ele in top2q19:
    tb = TextBlob(ele)
    pol_list2.append(tb.sentiment.polarity)

# Create a histogram with polarity score and count
plt.hist(pol_list2, bins=10)
plt.xlabel('Polarity Score')
plt.ylabel('Item Count')
plt.grid(True)
plt.savefig('hw2_ans19b_99007577.png')
plt.show()


# ### Question 20: Make outfile name format as `hw2_answers_(student_id).txt` and save it to `txt` file                
# - When you write the answer, please keep format(please refer to word doc example).
# - File name should be like this : <b>hw2_answers_37510930.txt</b>

# In[131]:


outfile = open('hw1_answers_{}.txt'.format(student_id), 'w')
outfile.write('{}, {}, {}\n'.format(last_name, first_name, email))
outfile.write("answer1={}\n".format(ans1))
outfile.write("answer2={}\n".format(ans2))
outfile.write("answer3={}\n".format(ans3))
outfile.write("answer4={}\n".format(ans4))
outfile.write("answer5={}\n".format(ans5))
outfile.write("answer6={}\n".format(ans6))
outfile.write("answer7={}\n".format(ans7))
outfile.write("answer8={}\n".format(ans8))
outfile.write("answer9={}\n".format(ans9))
outfile.write("answer10={}\n".format(ans10))
outfile.write("answer11={}\n".format(ans11))
outfile.write("answer12={}\n".format(ans12))
outfile.write("answer13={}\n".format(ans13))
outfile.write("answer14={}\n".format(ans14))
outfile.write("answer15={}\n".format(ans15))
outfile.write("HW 2 is done!!!\n")
outfile.close()


# #### After finishing `hw2`, please submit this python code file on Canvas!!
# #### But, you don't need to submit the `.png` files. 
# 
# #### Again, the code file name should be as follows: `hw2_(student_id).py` 
# (e.g.) hw2_37510930.py
