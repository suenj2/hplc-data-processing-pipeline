import file_reader
import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self, df_chunk):
        self.df = df_chunk
        self.starting_coordinate = (df_chunk.index.min(), int(df_chunk.columns.min()))
        self.row_size, self.col_size = df_chunk.shape

        # print(self.starting_coordinate)
        # print(self.row_size)
        # print(self.col_size)

    def __str__(self):
        return f"DataProcessor holding DataFrame:\n{self.df}"

    def pre_format(self):
        for rows in range(self.row_size):
            for cols in range(7, self.col_size):
                self.df.iloc[rows, cols] = np.nan

        self.df.iloc[0, 8] = "LINEST"
        self.df.iloc[1, 7] = "ratio"


