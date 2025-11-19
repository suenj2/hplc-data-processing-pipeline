import pandas as pd
import os

from super_file_loader import SuperFileLoader

class ConcFileLoader(SuperFileLoader):
    def __init__(self, file_path, sheet_name=None):
        super().__init__(file_path, sheet_name=sheet_name)
