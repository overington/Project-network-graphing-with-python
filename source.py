import pandas as pd
import networkx as nx
from pathlib import Path


def get_hash(row):
    return hash((row['Easting'], row['Northing']))


def get_region_df(file_name=False):
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
    else:
        file_name = 'data/{}'.format(file_name)
    df = pd.read_csv(file_name)

    # Collect  yearly data for each road
    df['road_section_hash'] = df.apply(get_hash, axis=1)
    #  year_range = df['AADFYear'].unique
    #  newdf = pd.DatetimeIndex(year_range)
    #  grouper = pd.Grouper(key='AADFYear', freq='1Y')

    #  df['normed'] = df.groupby(grouper)
    return df


def get_graph(df, G=nx.Graph):
    """
    split-apply-combine dataframe
    returns: graph
    """

    G = nx.Graph()

    G.add_nodes_from(df['road_id'])
    G.add_edges_from(df[['StartJunction', 'EndJunction']].values)
    return
