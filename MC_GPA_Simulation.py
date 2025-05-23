#!/usr/bin/env python
# coding: utf-8

# In[1]:


n = 100 #students
s = 100 #semesters


# In[2]:


import numpy as np
import pandas as pd
import matplotlib as mpl


# In[3]:


import matplotlib.pyplot as plt
from pandas.plotting import table


# In[4]:


#importing historical grade counts
hist_grade_dist = pd.read_csv('TUG_Grade_Distribution.csv')


# In[7]:

letterGrade = hist_grade_dist.iloc[0:12,:]


# In[9]:


gradePoint_dict = {'A':4,'A-':3.7,
                   'B+':3.3,'B':3,'B-':2.7,
                   'C+':2.3,'C':2,'C-':1.7,
                   'D+':1.3,'D':1,'D-':0.7,
                  'F':0}


# In[10]:
x = letterGrade['Grade'].map(gradePoint_dict)
letterGrade['gradePoint'] = x

# In[12]:

countTotal = letterGrade['Count'].sum()
x = letterGrade['Count'].map(lambda s: s / countTotal)
letterGrade['CountPercent'] = x


# In[14]:

x = letterGrade.loc[:,'CountPercent'].cumsum()
letterGrade['CountPercent_Cumu'] = x


# In[21]:


sim_list = [] #hold arrays of students
x = pd.DataFrame(columns=['Average GPA No Drop',
                          'Average GPA with Drop'],
                 index=['Semester']) 
mean_frame = x
#keeps track of summary statistics
#through the semesters

# In[23]:


def grade_choice():
    return np.random.choice([0,1,2,3,4])


# In[24]:


points = list(letterGrade['gradePoint'])
percent = list(letterGrade['CountPercent'])
#points , percent


# In[25]:


def historical_grade_choice(points,perc):
    return np.random.choice(points,p=perc)


# In[26]:


def num_classes():
    return np.random.choice([3,4,5])


# In[27]:


def drop_badGrade(ls):
    if any(ls < 2):
        y = [x for item in 
             np.argwhere(ls < 2).tolist() 
             for x in item]
        drop_index = np.random.choice(y)
        return np.delete(ls,drop_index)
    else: return ls
    


# In[28]:


arr = []
test = []
sim_list.clear()

#number of semesters / simulations
for i in np.arange(s): 
    for _ in np.arange(n): #number of students
        for _ in np.arange(num_classes()):
            #arr.append(grade_choice())
            arr.append(
                historical_grade_choice(points,percent)
                )
        
        sim_list.append(np.array(arr.copy()))
        arr.clear()
    
    test.append( [
     np.mean([np.mean(student) for 
              student in sim_list]), 
     np.mean([np.mean(drop_badGrade(student)) for 
              student in sim_list])
    ])

    sim_list.clear() #clear sim_list every semester

#index=pd.RangeIndex(start=1, stop=s, name='Semesters')
x = pd.DataFrame(test,
                 columns=['Average GPA No Drop',
                          'Average GPA with Drop'])
mean_frame = x

# In[30]:


mean_frame.index_name = 'Semesters'


# In[32]:

x = mean_frame.loc[:,'Average GPA with Drop']
y = mean_frame.loc[:,'Average GPA No Drop']
mean_frame['Differential'] = x - y


# In[33]:

#How much of percentage is due to artificial increase?
mean_frame['Percent Increase'] = (x - y) / y * 100


# In[35]:


mean_frame.loc[:,'Percent Increase'].mean() 

