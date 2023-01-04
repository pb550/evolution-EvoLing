var_data1 = {"year": ["before 1985", "1985-2005", "2006-2020"], "node_size": [90, 406, 1455], "edge_size": [109, 517, 2706], "giant_component_nodes": [25, 299, 1347], "giant_component_edges": [34, 423, 2619] }
var_var_before_1985 = pd.DataFrame(var_data1)

var_data2 = {"year": [2018, 2016, 2017, 2012, 2013, 2014, 2008, 1995, 2010, 2007, 2015, 1999], 
             "giant_component_size": [39, 21, 16, 22, 48, 14, 17, 61, 9, 16, 14, 26]}
giant_component_over_time = pd.DataFrame(var_data2)

# giant component size corresponding to each year as per our network graph
var_data2 = {"year": [1886,1931,1935,1960,1967,1968,1969,1970,1971,1974,1975,1981,1982,1983,1984,1985,1986,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020], 
             "giant_component_size": [2, 6, 7, 8, 16, 16, 16, 16, 18, 21, 25, 25, 25, 26, 27, 38, 44, 44, 53, 53, 59, 70, 82, 82, 166, 178, 188, 232, 274, 290, 294, 297, 334, 363, 371, 416, 474, 525, 572, 629, 680, 791, 891, 976, 1030, 1176, 1307, 1568, 1613, 1619]}
giant_component_over_time = pd.DataFrame(var_data2)

# graph of giant component over time
giant_component_over_time[giant_component_over_time['year'] >= 1980].plot(x= 'year', y = 'giant_component_size')
