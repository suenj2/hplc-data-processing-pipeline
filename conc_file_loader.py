import pandas as pd
import os

from super_file_loader import SuperFileLoader

class ConcFileLoader:
    def __init__(self, file_path):
        super().__init__(file_path)

    def extract_exp_df(self, exp_num):
        # df_conc =
        # df_chunk_extracted = self.df.iloc[row_min:row_max + 1, 0:14]
        return False
        # return df_chunk_extracted

# reader = ConcFileLoader("input/concentration.csv")
# ConcFileLoader.read_file_meta_data(reader)

