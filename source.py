import pandas as pd
import networkx as nx
from pathlib import Path



def get_region_data(file_name=False):
    """
    Get relevent CSV file,
    parse years
    add nodes or edges for each datapoint
    """
    if file_name is False:
        p = Path('data/')
        file_list = list(p.glob('*.csv'))
        file_list.sort()
        file_name = file_list[0]

    return pd.read_csv(file_name)


def get_graph(df,G=nx.Graph):
    """
    split-apply-combine dataframe
    returns: graph
    """
    
    