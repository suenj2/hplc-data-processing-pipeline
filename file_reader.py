import pandas as pd

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

    # def exp_start_cell(self, exp_num):
    #     for rows in range(self.num_rows):
    #         cell = self.df.iloc[rows, 0]
    #         if isinstance(cell, str) and f"Compound {exp_num}" in cell:
    #             print(f"Found {cell} at ")

    # def exp_row_range(self):
    #
    #     return (row_min, row_max)

    # def print_exp_raw(self, exp_num):
    #
    #     return False

reader = FileReader("input.xlsx", sheet_name="PFAS Kitcholm soils 3,4")
FileReader.read_file_meta_data(reader)
# FileReader.list_exps(reader)





# xlsx format is fucked need to write a function with a for loop to find cell A1
# Will also need a global var for these