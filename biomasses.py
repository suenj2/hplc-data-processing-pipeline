import pandas as pd
import numpy as np
from scipy.ndimage import extrema

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

class Biomasses:
    def __init__(self, input_df):
        self.input_df = input_df
        self.row_size, self.col_size = self.input_df.shape
        self.biomass_dict = self.extract_biomass_dict()
        self.sample_list = self.extract_sample_list()
        self.sample_list_header = ["Analytes"] + self.sample_list

    def extract_biomass_dict(self):
        biomass_dict = {}
        for row in range(self.row_size):
            biomass_dict[self.input_df.iloc[row, 0]] = self.input_df.iloc[row, 1]
        return biomass_dict

    def extract_sample_list(self):
        sample_list = []
        for row in range(self.row_size):
            sample_name = self.input_df.iloc[row, 0]
            sample_name_prefix = sample_name[:-1]
            if sample_name_prefix not in sample_list and not sample_name_prefix.startswith("SS"):
                sample_list.append(sample_name_prefix)
        return sample_list

