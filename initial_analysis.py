# import the relevant libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

# importing all the csv
authors = pd.read_csv('Authors.csv')
causal_links = pd.read_csv('CausalLinks.csv')
contributors = pd.read_csv('Contributors.csv')
documents = pd.read_csv('Documents.csv')
processes = pd.read_csv('Processes.csv')
variables = pd.read_csv('Variables.csv')
version = pd.read_csv('Version.csv')

# get the research papers from a specific time range
def doc_time_range(start_year, end_year):
    return(documents[(documents['year'] >= start_year) &  (documents['year'] <= end_year)])
  
# get authors files for a time range
def auth_time_range(start_year, end_year):
    auth = {"name": [], "bibref": []}
    doc = doc_time_range(start_year, end_year)

    for i in range(authors.shape[0]):
        if authors['bibref'][i] in list(doc['pk']):
            auth["name"].append(authors['name'][i])
            auth["bibref"].append(authors['bibref'][i])
            
    return(pd.DataFrame(auth))
  
# This will be same for all kinds of networks
# To cehck how many variables were discussed before 1984
# append year in causal_links

causal_links_year = causal_links

year = []
l = causal_links_year.shape[0]

for i in range(l):
    x = documents[documents['pk'] == causal_links_year.iloc[i]['bibref']].iloc[0]['year']
    year.append(x)

# Add year as a column
causal_links_year['Year'] = year

# get causal relationships for variables for a time range
def cl_time_range(start_year, end_year):
    return(causal_links_year[(causal_links_year['Year'] >= start_year) & (causal_links_year['Year'] <= end_year)])
  
# Initial Analysis
auth_per_paper = authors
year = []

# count number of auhtors corresponding to each paper
for i in range(auth_per_paper.shape[0]):
    doc = auth_per_paper['bibref'][i]
    df = documents[documents['pk'] == doc]
    y = df.iloc[0]['year']
    year.append(y)

auth_per_paper['year'] = year

auth_per_paper = pd.DataFrame(auth_per_paper.groupby(['year', 'bibref']).name.size())

auth_per_paper = pd.DataFrame(auth_per_paper.groupby(['year']).name.mean())

auth_per_paper = auth_per_paper['name'].round().reset_index()

auth_per_paper = auth_per_paper.rename(columns = {'name': 'authors_per_paper'})

# a scatter plot of average number of authors per paper each year - to understand collaboration over time
auth_per_paper.plot.scatter(x = 'year', y = 'authors_per_paper', title = 'Average number of authors per paper each year')

# plot papers published each year
doc_each_year.plot.scatter(x = 'year', y = 'papers', title = 'Distribution of papers published each year')












    
    
