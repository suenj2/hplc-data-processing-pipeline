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

    # Step 6: Append Biosolids Mass to the top left of dataframe
    biosolid_dict = {
        "SS1": 1.0846,
        "SS2": 1.0726,
        "SS3": 1.1534,

        "K4-1A": 1.0267,
        "K4-1B": 1.1481,
        "K4-1C": 1.0402,

        "K4-2A": 1.127,
        "K4-2B": 1.1154,
        "K4-2C": 1.1711,

        "K4-4A": 1.0932,
        "K4-4B": 1.15,
        "K4-4C": 1.0482,

        "K4-5A": 1.1054,
        "K4-5B": 1.0463,
        "K4-5C": 1.1155,

        "K3-1A": 1.0874,
        "K3-1B": 1.0898,
        "K3-1C": 1.0536,

        "K3-2A": 1.1218,
        "K3-2B": 1.198,
        "K3-2C": 1.1538,

        "K3-3A": 1.1183,
        "K3-3B": 1.1448,
        "K3-3C": 1.0493,

        "K3-4A": 1.0704,
        "K3-4B": 1.1589,
        "K3-4C": 1.0206,

        "K3-6A": 1.1289,
        "K3-6B": 1.195,
        "K3-6C": 1.1716
    } #Hardcoded for now. Remains the same for entire HPLC run. Need format of user input
    processing_df_chunk.set_biosolid_masses(biosolid_dict)

    # Step 7: Processing of data frame (append concentration)
    processing_df_chunk.pre_format()
    processing_df_chunk.append_std_conc(concentration_dict)
    processing_df_chunk.append_biosolid_masses() #Hardcoded for now. Masses change depends on experiment
    processing_df_chunk.ratio_calc()
    processing_df_chunk.linest()
    processing_df_chunk.conc_vial_calc()
    processing_df_chunk.corr_conc_calc()
    processing_df_chunk.conc_soil_calc()
    # processing_df_chunk.average_calc()
    print(processing_df_chunk)

    # print(processing_chunk)
