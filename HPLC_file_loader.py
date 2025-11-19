import pandas as pd

from super_file_loader import SuperFileLoader
from cell_coordinate_converter import CellCoordinateConverter

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

class HPLCFileLoader(SuperFileLoader):
    def __init__(self, file_path, sheet_name):
        super().__init__(file_path, sheet_name=sheet_name)

    def copy_file(self):
        return False

    def list_exps(self):
        for rows in range(self.num_rows):
            cell = self.df.iloc[rows, 0]
            if isinstance(cell, str) and "Compound" in cell:
                print(cell)

    def get_last_exp(self):
        col_values = self.df.iloc[:, 0]
        mask = col_values.apply(lambda x: isinstance(x, str) and "Compound" in x)
        filtered = col_values[mask]
        if not filtered.empty:
            exp_title = filtered.iloc[-1]

            # split by ":"
            split_colon = exp_title.split(":", 1)
            left = split_colon[0]

            # extract experiment number from the left
            return int(left.split(" ")[1])

    def exp_start_cell(self, exp_num):
        for rows in range(self.num_rows):
            cell = self.df.iloc[rows, 0]
            if isinstance(cell, str) and f"Compound {exp_num}" in cell:
                print(f'Found "{cell}" at cell location: {CellCoordinateConverter.to_excel_coord(0, rows)}')
                return (rows, 0)
        # print(f"Experiment number {exp_num} not found")
        raise ValueError(f"Experiment number {exp_num} not found in data.")

    def exp_row_range(self, exp_num):
        (title_row , title_col) = self.exp_start_cell(exp_num)
        row_min = title_row
        row_max = row_min + 3
        # while not pd.isna(self.df.iloc[row_max, 0]):
        while row_max < self.num_rows and not pd.isna(self.df.iat[row_max, 0]):
            row_max += 1
        return (row_min, row_max-1)

    def extract_df(self, exp_num):
        (row_min, row_max) = self.exp_row_range(exp_num)
        df_chunk_extracted = self.df.iloc[row_min:row_max+1, 0:18]
        return df_chunk_extracted
