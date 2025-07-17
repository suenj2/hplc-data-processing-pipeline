class ConcLib():
    def __init__(self, df_conc):
        self.df_conc = df_conc
        self.dict = {}
        self.row_size, self.col_size = df_conc.shape

    def load_dict(self):
        for col in range(self.col_size):
            compound_name = self.df_conc.iloc[0, col]
            sub_df_concs = self.df_conc.iloc[1:, [col]]
            self.dict[compound_name] = sub_df_concs
        return self.dict


