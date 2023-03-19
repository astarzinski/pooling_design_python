import pandas as pd
import time
from time import strftime
import os
import csv

#Sets the working directory to the folder in which this .py file resides.
def directory_set_and_folder_creation():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #Creates destination folders inside this working directory if they do not exist.
    if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/Output'):
        os.makedirs(os.path.dirname(os.path.abspath(__file__)) + '/Output')

def file_identification():
    file_name_dict = {}
    file_index = 1
    for file in os.listdir(os.getcwd()):
        if '.csv' in file:
            print(f'{file_index}: {file}')
            file_name_dict[file_index] = file
            file_index += 1
    while True:
        selected_file = input("Enter the integer associated with the sample list file.")
        try:
            selected_file = int(selected_file)
            break
        except:
            print('The value entered is not recognized as an integer')
    sample_list_file = file_name_dict[selected_file]
    return sample_list_file

def user_provided_sample_list_to_patient_array(s_list):
    df = pd.read_csv(s_list)
    print(df)
    
    return df

def unique_patient_data(upd_sd):
    unique_patient_list = []
    unique_patient_sample_dict = {}
    for key in upd_sd:
        if not upd_sd[key]['patient'] in unique_patient_list:
            unique_patient_list.append(upd_sd[key]['patient'])
    unique_patient_list.sort()
    #print(unique_patient_list)
    x = 1
    for patient_id in unique_patient_list:
        unique_patient_sample_dict[x] = {'patient' : patient_id, 'samples' : []}
        x += 1
    #print(unique_patient_sample_dict)
    for key_1 in upd_sd:
        for key_2 in unique_patient_sample_dict:
            if upd_sd[key_1]['patient'] == unique_patient_sample_dict[key_2]['patient']:
                unique_patient_sample_dict[key_2]['samples'].append(key_1)
                break
    #print(unique_patient_sample_dict)
    unique_patient_sample_dict =  dict(sorted(unique_patient_sample_dict.items(), key=lambda unique_patient_sample_dict: unique_patient_sample_dict[1]['count'], reverse = True))
    print(unique_patient_sample_dict)
def main():
    start_time = time.time()
    directory_set_and_folder_creation()
    user_sample_list = file_identification()
    sample_data_list = user_provided_sample_list_to_patient_array(user_sample_list)
    unique_patient_data(sample_data_list)
    print(f"\n--- {(time.time() - start_time):.2f} seconds ---\n")
main()