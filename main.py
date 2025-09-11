#Import libraries
import shutil
import pandas as pd

#Import classes
import os
import HPLC_file_loader
import biomasses
import conc_file_loader
import conc_lib
import data_processor
import file_writer
from summary_report import SummaryReport

#Pandas settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def filename_output(str_input):
    return str_input + "_processed"

def file_copy(src, dst):
    shutil.copy(src, dst)
    print(f"File successfully copied from {src} to {dst}")

def run_single_compound(exp_num):
    # Step 1: Make secure copy in output folder
    input_HPLC_filename = "input"  # hardcoded for now
    output_filename = filename_output(input_HPLC_filename)
    file_copy(f"input/{input_HPLC_filename}.xlsx", f"output/{output_filename}.xlsx")

    # Step 2: Open and extract dataframe from HPLC file (.xlsx) in output folder
    sheet_name_input = "PFAS Kitcholm soils 3,4"  # hardcoded for now
    HPLC_df = HPLC_file_loader.HPLCFileLoader(f"output/{output_filename}.xlsx", sheet_name=f"{sheet_name_input}")
    HPLC_df.read_file_meta_data()
    # HPLC_df.list_exps()

    # Step 3: Open and extract dataframe from compound concentration file (.csv) in output folder
    conc_file_name = "concentration w spikes"
    conc_sheet_name = "concentration"
    conc_df = conc_file_loader.ConcFileLoader(f"input/{conc_file_name}.xlsx", sheet_name=f"{conc_sheet_name}").df
    # print(conc_df)

    # Step 4: Load concentration library
    lib = conc_lib.ConcLib(conc_df)
    concentration_dict = lib.load_dict()
    # print(concentration_dict)

    # Step 5: Load HPLC data as a dataframe in the data_processor class.
    experiment_num = 3  # hardcoded for now
    df_chunk = HPLC_df.extract_df(experiment_num)
    processing_df_chunk = data_processor.DataProcessor(df_chunk)  # convert to data_processor object
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
    }  # Hardcoded for now. Remains the same for entire HPLC run. Need format of user input
    processing_df_chunk.set_biosolid_masses(biosolid_dict)

    # Step 7: Processing of data frame (append concentration)
    processing_df_chunk.process_all_steps(concentration_dict, )
    # print(processing_df_chunk)

    # Step 8: Append to HPLC_df
    processing_df_chunk.write_chunk_to_df(HPLC_df.df)
    print(HPLC_df)

    # Step 9: Write to .xlsx file
    file_writer.FileWriter.write_df_to_excel(processing_df_chunk.df, "output/input_processed.xlsx",
                                             "PFAS Kitcholm soils 3,4", processing_df_chunk.starting_coordinate[0],
                                             processing_df_chunk.starting_coordinate[1])

def run_all_compounds():
    # Step 1: Make secure copy in output folder
    input_HPLC_filename = "input"  # hardcoded for now
    output_filename = filename_output(input_HPLC_filename)
    file_copy(f"input/{input_HPLC_filename}.xlsx", f"output/{output_filename}.xlsx")

    # Step 2: Open and extract dataframe from HPLC file (.xlsx) in output folder
    HPLC_sheet_name = "PFAS Kitcholm soils 3,4"  # hardcoded for now
    HPLC_df = HPLC_file_loader.HPLCFileLoader(f"output/{output_filename}.xlsx", sheet_name=f"{HPLC_sheet_name}")
    HPLC_df.read_file_meta_data()
    last_exp_num = HPLC_df.get_last_exp()
    # HPLC_df.list_exps()

    # Step 3: Open and extract dataframe from compound concentration file (.csv) in output folder
    conc_file_name = "concentration w spikes"
    conc_sheet_name = "concentration"
    conc_df = conc_file_loader.ConcFileLoader(f"input/{conc_file_name}.xlsx", sheet_name=f"{conc_sheet_name}").df
    # print(conc_df)

    # Step 4: Load concentration library
    lib = conc_lib.ConcLib(conc_df)
    concentration_dict = lib.load_dict()
    # print(concentration_dict)

    # Step 5: Load biosolid_dict
    biosolid_mass_sheet_name = "Biosolid mass"
    biosolid_df = HPLC_file_loader.HPLCFileLoader(f"output/{output_filename}.xlsx", sheet_name=f"{biosolid_mass_sheet_name}")
    biomass_data = biomasses.Biomasses(biosolid_df.df)
    biosolid_dict = biomass_data.biomass_dict

    # biosolid_dict = {
    #     "SS1": 1.0846,
    #     "SS2": 1.0726,
    #     "SS3": 1.1534,
    #
    #     "K4-1A": 1.0267,
    #     "K4-1B": 1.1481,
    #     "K4-1C": 1.0402,
    #
    #     "K4-2A": 1.127,
    #     "K4-2B": 1.1154,
    #     "K4-2C": 1.1711,
    #
    #     "K4-4A": 1.0932,
    #     "K4-4B": 1.15,
    #     "K4-4C": 1.0482,
    #
    #     "K4-5A": 1.1054,
    #     "K4-5B": 1.0463,
    #     "K4-5C": 1.1155,
    #
    #     "K3-1A": 1.0874,
    #     "K3-1B": 1.0898,
    #     "K3-1C": 1.0536,
    #
    #     "K3-2A": 1.1218,
    #     "K3-2B": 1.198,
    #     "K3-2C": 1.1538,
    #
    #     "K3-3A": 1.1183,
    #     "K3-3B": 1.1448,
    #     "K3-3C": 1.0493,
    #
    #     "K3-4A": 1.0704,
    #     "K3-4B": 1.1589,
    #     "K3-4C": 1.0206,
    #
    #     "K3-6A": 1.1289,
    #     "K3-6B": 1.195,
    #     "K3-6C": 1.1716
    # } #Hard coded. User to input this per sheet

    # Step 6: Create summary dataframe
    default_sample_list = biomass_data.sample_list_header
    summary_df = SummaryReport(default_sample_list)
    summary_df.append_headers()
    print(default_sample_list)

    # default_sample_list = ["Analytes", "K4-1", "K4-2", "K4-4", "K4-5", "K3-1", "K3-2", "K3-3", "K3-4", "K3-6"] ##Hard coded. User to input this. Else loop for this default
    # summary_df = SummaryReport(default_sample_list)
    # summary_df.append_headers()

    # Step 7: For loop that loads and processes individual experiments
    # Step 7a: Load HPLC data as a dataframe in the data_processor class.
    # Step 7b: Process dataframe of specific compound.
    # Step 7c: Add dataframe to main HPLC_df dataframe.
    for exp in range(1, last_exp_num + 1):
        df_chunk = HPLC_df.extract_df(exp)
        processing_df_chunk = data_processor.DataProcessor(df_chunk)  # convert to data_processor object

        if processing_df_chunk.is_exp():
            try:
                processing_df_chunk.set_biosolid_masses(biosolid_dict)
                processing_df_chunk.process_all_steps(concentration_dict)
                processing_df_chunk.write_chunk_to_df(HPLC_df.df)
                summary_df.summary_extraction(processing_df_chunk)
            except Exception as e:
                print(f"❌ Error processing experiment {exps}: {e}")
                import traceback
                traceback.print_exc()

    # Step 8: Write HPLC_df.df dataframe to .xlsx file
    file_writer.FileWriter.write_df_to_excel(HPLC_df.df, "output/input_processed.xlsx", "PFAS Kitcholm soils 3,4", 0, 0)

    # Step 9: Write summary dataframe to .csv file
    summary_df_pd_format = summary_df.to_dataframe()
    os.makedirs("output", exist_ok=True) # NOT REQUIRED!!
    file_writer.FileWriter.write_df_to_excel(summary_df_pd_format, "output/summary.xlsx", "Summary", 0, 0)

if __name__ == '__main__':
    # run_single_compound(3)
    run_all_compounds()