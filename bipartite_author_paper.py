# Nodes

def author_document_nodes(start_year, end_year):
    doc_df = doc_time_range(start_year, end_year)
    doc = doc_df['pk']
    doc = pd.DataFrame(doc) # df of all the document Ids in 
    doc = doc.rename(columns={'pk': "Label"})
    doc['Type'] = 'document'
    
    auth = auth_time_range(start_year, end_year)
    auth_names = auth['name']
    auth_names = pd.DataFrame(auth_names)
    auth_names = auth_names.rename(columns={"name": "Label"}) # rename name as 'Label' for nodes table
    # add a column for type
    auth_names['Type'] = 'author'
    
    frames = [auth_names, doc]
    auth_doc_nodes = pd.concat(frames)
    # reset index
    auth_doc_nodes = auth_doc_nodes.reset_index()
    # the number of ids to be added - we'll arrange ids from 1 to 105 using pandas dataframe
    l = len(auth_doc_nodes['Label']) + 1
    # arrange the ids and add a column 'ID'
    auth_doc_nodes['ID'] = pd.Series(np.arange(1,l,1))
    # reindex the last column to first place
    auth_doc_nodes = auth_doc_nodes.reindex(['ID','Label','Type'], axis=1)
    
    return auth_doc_nodes

def author_document_edges(start_year, end_year):
    # this information is in - authors table
    auth_doc = auth_time_range(start_year, end_year)
    auth_doc = auth_doc.rename(columns={"name": "author", "bibref": "document"})
    
    # create source target lists and make the final edges dataframe
    source_auth_doc = []
    target_auth_doc = []
    
    for i in range(auth_doc.shape[0]):
        auth_doc_nodes = author_document_nodes(start_year, end_year)
        x = auth_doc_nodes[auth_doc_nodes['Label'] == auth_doc['author'].iloc[i]].iloc[0]['ID']
        source_auth_doc.append(x)
        y = auth_doc_nodes[auth_doc_nodes['Label'] == auth_doc['document'].iloc[i]].iloc[0]['ID']
        target_auth_doc.append(y)
        
    data = {"Source": source_auth_doc, "Target": target_auth_doc}
    auth_doc_edges = pd.DataFrame(data)
    
    return auth_doc_edges

nodes = author_document_nodes(1886,2022)
edges = author_document_edges(1886,2022)
start_year = 1886
end_year = 2022
network_type = "doc_auth"
convert_to_csv(nodes, edges, start_year, end_year, network_type)
