#Import libraries
import shutil
import pandas as pd

#Import classes
import HPLC_file_loader
import conc_file_loader
import conc_lib
import data_processor

def filename_output(str_input):
    return str_input + "_processed"

def file_copy(src, dst):
    shutil.copy(src, dst)
    print(f"File successfully copied from {src} to {dst}")

if __name__ == '__main__':
    # Step 1: Make secure copy in output folder
    input_HPLC_filename = "input" #hardcoded for now
    output_filename = filename_output(input_HPLC_filename)
    file_copy(f"input/{input_HPLC_filename}.xlsx", f"output/{output_filename}.xlsx")

    # Step 2: Open and extract dataframe from HPLC file (.xlsx) in output folder
    sheet_name_input = "PFAS Kitcholm soils 3,4" #hardcoded for now
    HPLC_df = HPLC_file_loader.HPLCFileLoader(f"output/{output_filename}.xlsx", sheet_name=f"{sheet_name_input}")
    HPLC_df.read_file_meta_data()
    # HPLC_df.list_exps()

    # Step 3: Open and extract dataframe from compound concentration file (.csv) in output folder
    conc_file_name = "concentration"
    conc_df = conc_file_loader.ConcFileLoader(f"input/{conc_file_name}.csv").df
    # print(conc_df)

    # Step 4: Load concentration library
    lib = conc_lib.ConcLib(conc_df)
    concentration_dict = lib.load_dict()
    # print(concentration_dict)

    # Step 5: Load HPLC data as a dataframe in the data_processor class.
    experiment_num = 1 #hardcoded for now
    df_chunk = HPLC_df.extract_df(experiment_num)
    processing_df_chunk = data_processor.DataProcessor(df_chunk) #convert to data_processor object
    # print(processing_df_chunk)

    # Step 6: Processing of data frame (append concentration)
    processing_df_chunk.append_std_conc(concentration_dict)
    processing_df_chunk.pre_format()
    processing_df_chunk.ratio_calc()
    processing_df_chunk.linest()
    processing_df_chunk.conc_vial_calc()
    processing_df_chunk.corr_conc_calc()
    processing_df_chunk.conc_soil_calc()
    processing_df_chunk.average_calc()
    print(processing_df_chunk)

    # print(processing_chunk)
