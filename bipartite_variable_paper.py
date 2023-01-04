def variable_document_relation(start_year, end_year):    
    cl_var1 = cl_time_range(start_year, end_year)[['Var1', 'bibref']] # a df with only Var1 and document id columns
    cl_var2 = cl_time_range(start_year, end_year)[['Var2', 'bibref']]
    
    cl_var1 = cl_var1.rename(columns={"Var1": "variable"})
    cl_var2 = cl_var2.rename(columns={"Var2": "variable"})
    
    # combine the above two dataframes to get a single dataframe with variable paper information
    var_doc = pd.concat([cl_var1, cl_var2], ignore_index=True)
    
    # since there is an overlap in Var1 and Var2, there are duplicate values in causal_links_year_before_1984_var_doc
    # this gives us the paper variable relationship
    var_doc = var_doc.drop_duplicates()
    
    variable_name = []
    
    for i in range(var_doc.shape[0]):
        x = variables[variables['pk'] == var_doc['variable'].iloc[i]].iloc[0]['name']
        variable_name.append(x)
        
    # Now we have a df with variable ids, names and papers
    var_doc['variable_name'] = variable_name
    return var_doc
  
# Nodes

# function for making a bipartite network 
def variable_document_nodes(start_year, end_year):
    doc_df = doc_time_range(start_year, end_year)
    doc = doc_df['pk']
    doc = pd.DataFrame(doc) # df of all the document Ids in 
    doc = doc.rename(columns={'pk': "Label"})
    doc['Type'] = 'document'
    var = var_unique_time_range(start_year, end_year)
    frames = [doc, var]
    # concat into a single dataframe
    var_doc_nodes = pd.concat(frames)

    # reset index
    var_doc_nodes = var_doc_nodes.reset_index()
    # the number of ids to be added - we'll arrange ids from 1 to 105 using pandas dataframe
    l = len(var_doc_nodes['Label']) + 1
    # arrange the ids and add a column 'ID'
    var_doc_nodes['ID'] = pd.Series(np.arange(1,l,1))
    # reindex the last column to first place
    var_doc_nodes = var_doc_nodes.reindex(['ID','Label','Type'], axis=1)
    return var_doc_nodes

# Edges

# We want edges that connect the paper to the variables it speaks about.
# We first make a dataframe of all the variables corresponding to each paper (this df gives the variable <-> relation)
def variable_document_edges(start_year, end_year):
    var_doc = variable_document_relation(start_year, end_year)
    
    # Make source and target lists and eventually the edges csv

    source_var_doc = []
    target_var_doc = []
    
    for i in range(var_doc.shape[0]):
        req_var_doc_nodes = variable_document_nodes(start_year, end_year)
        x = req_var_doc_nodes[req_var_doc_nodes['Label'] == var_doc['variable_name'].iloc[i]].iloc[0]['ID']
        source_var_doc.append(x)
        y = req_var_doc_nodes[req_var_doc_nodes['Label'] == var_doc['bibref'].iloc[i]].iloc[0]['ID']
        target_var_doc.append(y)
        
    data = {"Source": source_var_doc, "Target": target_var_doc}
    var_doc_edges = pd.DataFrame(data)
    
    return var_doc_edges    
  
nodes = variable_document_nodes(1886,2022)
edges = variable_document_edges(1886,2022)
start_year = 1886
end_year = 2022
network_type = "var_doc"
convert_to_csv(nodes, edges, start_year, end_year, network_type)
