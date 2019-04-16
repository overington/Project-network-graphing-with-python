import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
import random


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
        file_name = random.choice(file_list)
    else:
        file_name = 'data/{}'.format(file_name)
    df = pd.read_csv(file_name)

    # Collect  yearly data for each road
    df['road_section_hash'] = df.apply(get_hash, axis=1)
    return df


def get_graph(df, G=nx.Graph):
    """
    split-apply-combine dataframe
    returns: graph
    """

    G = nx.Graph()

    G.add_nodes_from(df['road_id'])
    G.add_edges_from(df[['StartJunction', 'EndJunction']].values)
    return G


def get_cat_year_data(df, filter_cat, filter_nme, col):
    """
    Filter df filter_cat[i] == filter_nme
    Collect all col data from per year
    """
    collected_data = []
    year_range = df['AADFYear'].unique()
    for year in year_range:
        collect_data = df[
            (df[filter_cat] == filter_nme) & (df.AADFYear == year)
        ]
        collected_data.append(collect_data.iloc[0][col])
    return year_range, collected_data


def get_year_data(df, road_hash, col):
    """
    return collected_data per year for road_hash
    """
    year_range, collected_data = get_cat_year_data(
        df,
        'road_section_hash',
        road_hash,
        col)
    return year_range, collected_data


def hash_single(df, hsh, col, n=0):
    """returns the nth cell value of hsh in df[col]  """
    years, road_name = get_year_data(df, hsh, col)
    return road_name[0]  # They all should be the same


def hash_to_name(df, hsh):
    road_name = hash_single(df, hsh, 'Road')
    startjunc = hash_single(df, hsh, 'StartJunction')
    endjunc = hash_single(df, hsh, 'EndJunction')
    return '{} ({} to {})'.format(
        road_name, startjunc, endjunc)  # They all should be the same


def filter_collect(df, filter_dict, grouping='AADFYear'):
    """
    Using fkey, fval from filter_dict.items
    Filter df filter_cat[i] == filter_name
    Collect all col data from per year
    """

    collected_data = dict()
    grouping_range = df[grouping].unique()
    for filter_cat, filter_name in filter_dict.items():
        for group in grouping_range:
            print('filter_name: ', filter_name)
            collected_data[group][filter_name] = df[(
                df[filter_cat] == filter_name
            ) & (
                df[grouping] == group  # this should be group_name
            )]
            print('done')

    #         collected_data[group] = collect_data.iloc[0][col]
    return collected_data


def plot_per_year(df, col_name, fig_title=None):
    hashes = df['road_section_hash'].unique()

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot(111)

    for road_hash in hashes:
        edge_df = df[df['road_section_hash'] == road_hash]

        name = '{}'.format(hash_to_name(edge_df, road_hash))
        year_range, collected = get_year_data(edge_df, road_hash, col_name)
        plt.plot(year_range, collected, label=name)

    if len(hashes) >= 6:
        box = ax.get_position()

        # Shrink current axis by 20%
        ax = plt.gca()  # ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        plt.legend()

    plt.grid()
    plt.title(fig_title)
    plt.xlabel('Year')
    plt.ylabel('Count')
    return fig


def net_graph(df):
    """
    create a network plot from the dataframe
    """
    G = nx.from_pandas_edgelist(
        df,
        source='StartJunction',
        target='EndJunction',
        edge_attr=True
    )
    return G


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    from itertools import filterfalse
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def li2n(li, f=np.linspace, f_min=0, f_max=1, **kwargs):
    """
    maps all unique list items (li) to numerical id
    li: iterable of hashable terms
    f: method of counting tems (eg: np.logspace)
    return: dict {li: num}
    """
    unique = [_ for _ in unique_everseen(li)]
    number_line = f(f_min, f_max, len(unique), **kwargs)
    return {key: val for key, val in zip(unique, number_line)}


def get_edge_weights(G, edge_attr, edges=False):
    if edges is False:
        edges = G.edges()
    return np.array([G[u][v][edge_attr] for u, v in edges])


def drw_graph_filtered(df,year,filter_col,cutoff):

    df_all = df[ (df['AADFYear']==year) & (df[filter_col]>= 0) ]
    df_filt = df[ (df[filter_col]>= cutoff) ]

    NX_all = net_graph(df_all)
    NX_heavy = net_graph(df_filt)

    pos_all = nx.drawing.nx_agraph.graphviz_layout( NX_all, prog='twopi')

    edges = NX_all.edges()
    road_list = [NX_all[u][v]['Road'] for u,v in edges]
    colours_dict = li2n(road_list)
    colours = []
    for road in road_list:
    #     Make each 'Road' attribute a different colour
        colours.append(colours_dict[road])

    labels = {}
    edge_attrs_cycles = nx.get_edge_attributes(NX_all, filter_col)
    edge_attrs_road = nx.get_edge_attributes(NX_all, 'Road')


    weights = get_edge_weights(NX_all, filter_col, edges)
    normalised_weights = weights/np.sort(weights)[-1]

    for edge in edges:
        if edge_attrs_cycles[edge]>= cutoff:
    #         only show 'heavy' road usage
            labels[edge] = edge_attrs_road[edge]

    nx.draw(
        NX_all,
        edges=edges,
        edge_color=colours,
        width=3*normalised_weights,
    #     edge_cmap=plt.cm.Paired,
        node_size=5,
        pos=pos_all)

def drw_graph(G,weight_attr,pos):
    """
    line_weight: column name for
    """
    edges = G.edges()
    road_list = [G[u][v]['Road'] for u,v in edges]
    colors_dict = li2n(road_list)
    colours = []
    for road in road_list:
        colours.append(colors_dict[road])

    weights = get_edge_weights(G, 'PedalCycles', edges)
    normalised_weights = weights/np.sort(weights)[-1]

    nx.draw(
        G,
        edges=edges,
        edge_color=colours,
        width=15*normalised_weights,
        edge_cmap=plt.cm.Paired,
        node_size=10,
        pos=pos
    )
