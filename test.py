from source import get_region_data

london_df = get_region_data('London.csv')

get_graph(london_df)

df = split('AADFYear', london_df)

graph = nx.Graph()

test = True