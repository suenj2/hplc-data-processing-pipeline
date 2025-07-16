import pandas as pd
import os

from super_file_loader import SuperFileLoader

class ConcFileLoader(SuperFileLoader):
    def __init__(self, file_path):
        super().__init__(file_path)

    def extract_exp_df(self):
        return self.df

# reader = ConcFileLoader("input/concentration.csv")
# ConcFileLoader.read_file_meta_data(reader)
