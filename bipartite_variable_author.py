# Nodes

def variable_author_nodes(start_year, end_year):
    auth = auth_time_range(start_year, end_year)
    auth_names = auth['name']
    auth_names = pd.DataFrame(auth_names)
    auth_names = auth_names.rename(columns={"name": "Label"}) # rename name as 'Label' for nodes table
    # add a column for type
    auth_names['Type'] = 'author'
    # get all the variable names in the given time range
    var = var_unique_time_range(start_year, end_year)
    frames = [auth_names, var]
    # concat into a single dataframe
    auth_var_nodes = pd.concat(frames)
    # reset index
    auth_var_nodes = auth_var_nodes.reset_index()
    # the number of ids to be added - we'll arrange ids in his range using pandas dataframe
    l = len(auth_var_nodes['Label']) + 1
    # arrange the ids and add a column 'ID'
    auth_var_nodes['ID'] = pd.Series(np.arange(1,l,1))
    # reindex the last column to first place
    auth_var_nodes = auth_var_nodes.reindex(['ID','Label','Type'], axis=1)
    
    return auth_var_nodes

# Edges 

def variable_author_edges(start_year, end_year):
    var_doc = variable_document_relation(start_year, end_year)
    auth = auth_time_range(start_year, end_year)
    # merged table gives info about variables their corresponding papers and their authors
    var_doc_auth_merged = pd.merge(var_doc, auth)
    var_auth = var_doc_auth_merged[["variable", "variable_name", "name"]]
    var_auth = var_auth.rename(columns={"name": "author"})
    
    # create source target lists and make the final edges dataframe
    source_var_auth = []
    target_var_auth = []
    
    for i in range(var_auth.shape[0]):
        var_auth_nodes = variable_author_nodes(start_year, end_year)
        x = var_auth_nodes[var_auth_nodes['Label'] == var_auth['variable_name'].iloc[i]].iloc[0]['ID']
        source_var_auth.append(x)
        y = var_auth_nodes[var_auth_nodes['Label'] == var_auth['author'].iloc[i]].iloc[0]['ID']
        target_var_auth.append(y)
        
    data = {"Source": source_var_auth, "Target": target_var_auth}
    var_auth_edges = pd.DataFrame(data)
    
    return var_auth_edges

nodes = variable_author_nodes(1886,2022)
edges = variable_author_edges(1886,2022)
start_year = 1886
end_year = 2022
network_type = "var_auth"
convert_to_csv(nodes, edges, start_year, end_year, network_type)

