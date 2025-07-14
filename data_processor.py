import file_reader
import pandas as pd

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
                # print(self.df.iloc[rows, cols])
                self.df.iloc[rows, cols] = pd.NA

        # self.df.iloc[self.rows+1, 8] = "LINEST"
        # self.df.iloc[self.rows+2, 7] = "ratio"
        # self.df.iloc[self.rows+2, 7] = "ratio"


