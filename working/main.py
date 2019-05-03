from src import filter_collect, plot_per_year, get_region_df,\
    get_cat_year_data, get_year_data, hash_single, hash_to_name, net_graph,\
    unique_everseen, li2n, get_edge_weights
from pathlib import Path
import random
import numpy as np

if __name__ == '__main__':

    metrics_li = ['PedalCycles', 'Motorcycles', 'CarsTaxis', 'BusesCoaches',
          'LightGoodsVehicles', 'V2AxleRigidHGV', 'V3AxleRigidHGV',
          'V4or5AxleRigidHGV', 'V3or4AxleArticHGV', 'V5AxleArticHGV',
          'V6orMoreAxleArticHGV', 'AllHGVs', 'AllMotorVehicles'
          ]

    region_df = get_region_df()  # Empty calls random choice
    for metric in metrics_li:
        A1 = region_df[region_df['Road']=='A1']
        yearly_fig = plot_per_year(A1, 'PedalCycles', 'PedalCycle traffic on sections of A1 from 2000 - 2017')
