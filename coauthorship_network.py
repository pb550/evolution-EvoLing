# filter out the rows where we have more than one author per paper, because we want to analyse collaborations
v = authors.bibref.value_counts()
# value counts for bibref is greater than 1
auth_colab = authors[authors.bibref.isin(v.index[v.gt(1)])]
auth_colab = auth_colab.reset_index()

# group by 'bibref' to get the list of all authors corresponding to each paper
group = auth_colab.groupby('bibref')
# extract list of all unique author names for each bibref or document
auth_colab_list = group.apply(lambda x: x['name'].unique())
auth_colab_list = auth_colab_list.reset_index()
auth_colab_list = auth_colab_list.rename(columns = {'bibref': 'document', 0 : 'authors'})

# create a pair wise combination of items in the list for all columns
auth_colab_list['authors'] = auth_colab_list['authors'].apply(lambda x: list(itertools.combinations(list(x), 2)))

# separate each elemet of list in separate records
auth_colab_list = auth_colab_list.explode('authors')

# create two columns for each tupple record (these would be source and targets)
auth_colab_edges = pd.concat([auth_colab_list,pd.DataFrame(auth_colab_list.pop('authors').tolist(),index=auth_colab_list.index)],axis=1)
auth_colab_edges = auth_colab_edges.rename(columns = {0: 'source', 1: 'target'})

# nodes for co-authorship network
auth_colab_nodes = auth_colab
auth_colab_nodes = auth_colab_nodes.drop(columns = ['index', 'bibref'])
auth_colab_nodes = auth_colab_nodes.drop_duplicates()
auth_colab_nodes = auth_colab_nodes.reset_index()
auth_colab_nodes = auth_colab_nodes.rename(columns = {'index': 'id', 'name': 'label'})

Source = []
Target = []
for i in range(auth_colab_edges.shape[0]):
    auth_id1 = auth_colab_nodes[auth_colab_nodes['label'] == auth_colab_edges['source'].iloc[i]].iloc[0]['id']
    Source.append(auth_id1)
    auth_id2 = auth_colab_nodes[auth_colab_nodes['label'] == auth_colab_edges['target'].iloc[i]].iloc[0]['id']
    Target.append(auth_id2)

auth_colab_edges['Source'] = Source    
auth_colab_edges['Target'] = Target 

auth_colab_edges = auth_colab_edges.drop(columns = ['source', 'target'])

# files ready to be imported to Gephi
auth_colab_nodes.to_csv('auth_colab_nodes.csv', index=False)
auth_colab_edges.to_csv('auth_colab_edges.csv', index=False)

