import pandas as pd

from cell_coordinate_converter import CellCoordinateConverter

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

class FileReader:
    def __init__(self, file_path, sheet_name=None):
        self.df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        self.num_rows, self.num_cols = self.df.shape

    def read_file_meta_data(self):
        print(f".xlsx file contains {self.num_rows} rows and {self.num_cols} columns.")

    def list_exps(self):
        for rows in range(self.num_rows):
            cell = self.df.iloc[rows, 0]
            if isinstance(cell, str) and "Compound" in cell:
                print(cell)

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
        row_min = title_row + 2
        # print(row_min)
        row_max = row_min + 1
        while not pd.isna(self.df.iloc[row_max, 0]):
            row_max += 1
        return (row_min, row_max-1)

    def extract_df(self, exp_num):
        (row_min, row_max) = self.exp_row_range(exp_num)
        df_chunk_extracted = self.df.iloc[row_min:row_max, 0:14]
        return df_chunk_extracted

reader = FileReader("input.xlsx", sheet_name="PFAS Kitcholm soils 3,4")
FileReader.read_file_meta_data(reader)
# FileReader.list_exps(reader)
# FileReader.exp_start_cell(reader, 1)
# FileReader.exp_start_cell(reader, 133)
# print(FileReader.exp_start_cell(reader, 1))
# print(FileReader.exp_row_range(reader, 1)) #should be (7,54)
# print(FileReader.extract_df(reader, 1))

# Will also need a global var for these