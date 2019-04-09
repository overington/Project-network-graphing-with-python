import pandas as pd
import networkx as nx

class TheData():
    def __init__(self, file_name=False):
        if file_name is False:
            from pathlib import Path
            p = Path('data/')
            file_list = list(p.glob('*.csv'))
            file_list.sort()
            file_name = file_list[0]
        self.df_raw = pd.read_csv(file_name)
        
        self.df = self.split('AADFYear', self.df_raw)
        
        self.graph = nx.Graph()
        
        """
        structure of df
        year; edge and node
        """
        
    def df_raw(self):
        return self.df_raw
    
    def split(self, col_name='AADFYear', df_in=False):
        if df_in is False:
            df_in = self.df_raw
        df_out = df_in.groupby(col_name)
        return df_out.groups
        
        
    
    def get_data(file_name=False):
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
    
    def get_year(self, col_name='AADFYear'):
        """Split DataFram `df` into years, using df."""
        return self.df.groupby([col_name])