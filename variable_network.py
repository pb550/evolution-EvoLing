# Edges
# Function takes the start year and end year as arguments and returns edges for variable <-> network

def variable_edges(start_year, end_year):
    cl = cl_time_range(start_year, end_year)
    var_edges = {'Source': cl['Var1'], 'Target': cl['Var2'], 'Relation': cl['Relation'], 'Cor': cl['Cor'], 
                'Timeset': cl['Year'], 'Topic': cl['Topic']}
    var_edges = pd.DataFrame(var_edges)
    return var_edges

# Nodes

def variable_nodes(start_year, end_year):
    cl = causal_links_year[(causal_links_year['Year'] >= start_year) & (causal_links_year['Year'] <= end_year)]
    var_edges = {'Source': cl['Var1'], 'Target': cl['Var2'], 'Relation': cl['Relation'], 'Cor': cl['Cor'], 
                'Year': cl['Year'], 'Topic': cl['Topic']}
    var_edges = pd.DataFrame(var_edges)
    var = list(var_edges['Source'])
    for i in range(len(var_edges['Target'])):
        z = var_edges.iloc[i]['Target']
        var.append(z)
    
# check what values from the entire list of variables_before_1984 match with variables to get the names for the 
# unique variables_before_1984 ids
    var_nodes = variables[variables['pk'].isin(var)]
    var_nodes = var_nodes.rename(columns={"pk":"ID", "name":"Label"})
    return var_nodes
  
# function that makes csv files for nodes and edges
def convert_to_csv(nodes, edges, start_year, end_year, network_type):
    nodes_csv = f"nodes_{network_type}_{start_year}_{end_year}.csv"
    edges_csv = f"edges_{network_type}_{start_year}_{end_year}.csv"
    file_nodes = nodes.to_csv(nodes_csv, index = False)
    file_edges = edges.to_csv(edges_csv, index = False)
    return file_nodes, file_edges
  
nodes = variable_nodes(1886,2022)
edges = variable_edges(1886,2022)
start_year = 1886
end_year = 2022
network_type = "var_var"
convert_to_csv(nodes, edges, start_year, end_year, network_type)

# to study network change over time, we need to associate each connection with time 
# this function assigns year to each connection

def variable_nodes_timeseries(start_year, end_year):
    cl = causal_links_year[(causal_links_year['Year'] >= start_year) & (causal_links_year['Year'] <= end_year)]
    var_edges = {'Source': cl['Var1'], 'Target': cl['Var2'], 'Relation': cl['Relation'], 'Cor': cl['Cor'], 
                'Year': cl['Year'], 'Topic': cl['Topic']}
    var_edges = pd.DataFrame(var_edges)
    var = list(var_edges['Source']) # list of all the source variables
    time = list(var_edges['Year'])  # list of all times corresponding to source
    
        # we use for loop to append the target nodes and the time corrresponding to each target node
    
    for i in range(len(var_edges['Target'])): 
        z = var_edges.iloc[i]['Target']
        t = var_edges.iloc[i]['Year']
        var.append(z)
        time.append(t)
        
    var_nodes = pd.DataFrame(({"ID": var, "Year": time}))
    label = []
    for i in range(var_nodes.shape[0]):
        v = var_nodes['ID'][i]
        label.append(variables[variables['pk'] == v].iloc[0]['name'])
    
    var_nodes['Label'] = label
    return var_nodes

  
# Variable variable network from 1886-1984
nodes = variable_nodes(1886,1984)
edges = variable_edges(1886,1984)
start_year = 1886
end_year = 1984
network_type = "var_var"
convert_to_csv(nodes, edges, start_year, end_year, network_type)  

# Variable variable network from 1985-2005
nodes = variable_nodes(1985,2005)
edges = variable_edges(1985,2005)
start_year = 1985
end_year = 2005
network_type = "var_var"
convert_to_csv(nodes, edges, start_year, end_year, network_type)


# Variable variable network from 2006-2020
nodes = variable_nodes(2006,2020)
edges = variable_edges(2006,2020)
start_year = 2006
end_year = 2020
network_type = "var_var"
convert_to_csv(nodes, edges, start_year, end_year, network_type)
