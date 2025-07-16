import pandas as pd
import os

class SuperFileLoader:
    def __init__(self, file_path, sheet_name=None):
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".csv":
            self.df = pd.read_csv(file_path, header=None)
        elif ext in (".xls", ".xlsx"):
            self.df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        self.num_rows, self.num_cols = self.df.shape

    def read_file_meta_data(self):
        print(f"File contains {self.num_rows} rows and {self.num_cols} columns.")
