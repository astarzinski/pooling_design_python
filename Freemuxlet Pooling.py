import pandas as pd
import time
import os
from itertools import combinations, permutations
import random
from datetime import datetime

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
        selected_file = input("Enter the integer associated with the sample list file.\n")
        try:
            selected_file = int(selected_file)
            break
        except:
            print('The value entered is not recognized as an integer')
    sample_list_file = file_name_dict[selected_file]
    return sample_list_file

def pad_generator(s_list):
    pool_assignment_dictionary = {}
    df = pd.read_csv(s_list)
    column_list = df.columns.tolist()
    unique_participants = df[column_list[0]].unique().tolist()
    for participant in unique_participants:
        pool_assignment_dictionary[participant] = {'Sample_IDs': {}, "Participant_Attributes": {}}
        participant_sample_count = 0
        for index, row in df.iterrows():
            if row['Participant ID'] == participant:
                pool_assignment_dictionary[participant]['Sample_IDs'][row['Sample ID']] = {'Pool': 0}
                participant_sample_count += 1
                if len(column_list) > 2:
                    for attribute in column_list[2:]:
                        if 'sample' in attribute.lower():
                            pool_assignment_dictionary[participant]['Sample_IDs'][row['Sample ID']][attribute] = [row[attribute]][0]
                        elif 'participant' in attribute.lower():
                            pool_assignment_dictionary[participant]["Participant_Attributes"][attribute] = [row[attribute]][0]
        pool_assignment_dictionary[participant]['Sample_Count'] = participant_sample_count
    #print(pool_assignment_dictionary)
    return pool_assignment_dictionary

def minimum_pools_with_control_in_all_pools(min_pools_pad):
    min_pools = 0
    for key in min_pools_pad:
        if min_pools_pad[key]['Sample_Count'] > min_pools:
            min_pools = min_pools_pad[key]['Sample_Count']
    min_pools += 1
    return min_pools

def user_determined_pool_count():
    while True:
        pool_count = input('If you have a desired number of pools\nenter the interger now.\nElse hit return.\n')
        if pool_count != '':
            try:
                pool_count = int(pool_count)
                return pool_count
            except:
                print(f'{pool_count} is not recognized as an integer!')
        return False

def pool_count_determination(i_c_g_pad):
    pools = user_determined_pool_count()
    if not pools:
        pools = minimum_pools_with_control_in_all_pools(i_c_g_pad)
    elif pools < minimum_pools_with_control_in_all_pools(i_c_g_pad):
        print('There are too many samples for one or more patients to use that few sample pools!')
        pools = minimum_pools_with_control_in_all_pools(i_c_g_pad)
    return pools

def combo_selection(c_s_pad, number_pools):
    pool_counter_dict = {}
    participant_attribute_counter = {}
    unique_combo_list = []
    for i in range(1, number_pools + 1):
        pool_counter_dict[i] = 0
        participant_attribute_counter[i] = {}
        for key in c_s_pad:
            for p_attribute in c_s_pad[key]["Participant_Attributes"]:
                if not p_attribute in participant_attribute_counter[i]:
                    participant_attribute_counter[i][p_attribute] = {}
                participant_attribute_counter[i][p_attribute][c_s_pad[key]["Participant_Attributes"][p_attribute]] = 0
    for key in c_s_pad:
        best_combo = ()
        lowest_combo_score = 1000000
        for combo in combinations(range(1, number_pools + 1), c_s_pad[key]['Sample_Count']):
            combo_score = 0
            if not combo in unique_combo_list:
                for pool_integer in combo:
                    combo_score += pool_counter_dict[pool_integer]
                    for p_att_key in participant_attribute_counter[pool_integer]:
                        combo_score += participant_attribute_counter[pool_integer][p_att_key][c_s_pad[key]["Participant_Attributes"][p_att_key]]
                if combo_score < lowest_combo_score:
                    lowest_combo_score = combo_score
                    best_combo = combo
        unique_combo_list.append(best_combo)
        for pool_integer in best_combo:
            pool_counter_dict[pool_integer] += 1
            for p_att_key in participant_attribute_counter[pool_integer]:
                participant_attribute_counter[pool_integer][p_att_key][c_s_pad[key]["Participant_Attributes"][p_att_key]] += 1
        c_s_pad[key]["Selected_Combo"] = best_combo
    print(pool_counter_dict)
    print(participant_attribute_counter)
    return(c_s_pad)

def permutation_selection(ps_pad, perm_pool_count):
    sample_attribut_counter = {}
    for i in range(1, perm_pool_count + 1):
        sample_attribut_counter[i] = {}
        for key in ps_pad:
            for sample in ps_pad[key]['Sample_IDs']:
                for s_attribute in ps_pad[key]['Sample_IDs'][sample]:
                    if s_attribute == 'Pool':
                        continue
                    else:
                        if not s_attribute in sample_attribut_counter[i]:
                            sample_attribut_counter[i][s_attribute] = {}
                        sample_attribut_counter[i][s_attribute][ps_pad[key]['Sample_IDs'][sample][s_attribute]] = 0
    for key in ps_pad:
        best_perm = ()
        lowest_perm_score = 1000000
        for perm in permutations(ps_pad[key]['Selected_Combo']):
            perm_score = 0
            for pool_integer, sample in zip(perm, ps_pad[key]['Sample_IDs']):
                for s_att_key in sample_attribut_counter[pool_integer]:
                    perm_score += sample_attribut_counter[pool_integer][s_att_key][ps_pad[key]['Sample_IDs'][sample][s_att_key]]
            if perm_score < lowest_perm_score:
                lowest_perm_score = perm_score
                best_perm = perm
        for pool_integer, sample in zip(best_perm, ps_pad[key]['Sample_IDs']):
            for s_att_key in sample_attribut_counter[pool_integer]:
                sample_attribut_counter[pool_integer][s_att_key][ps_pad[key]['Sample_IDs'][sample][s_att_key]] += 1
        ps_pad[key]["Selected_Perm"] = best_perm
    print(sample_attribut_counter)
    return(ps_pad)
        #print(list(permutations(ps_pad[key]['Selected_Combo'])))

def sample_assignment_to_pools(sap_pad):
    for key in sap_pad:
        pro_numerical_array = []
        numerical_array = []
        i = 0
        #Creates a sequential list from 0 to n-1.
        while i < sap_pad[key]['Sample_Count']:
            pro_numerical_array.append(i)
            i += 1
        #Selects random items from the ordered list to create a list without set ordering.
        while len(pro_numerical_array) > 0:
            pro_index = random.randint(0, (len(pro_numerical_array) - 1))
            numerical_array.append(pro_numerical_array.pop(pro_index))
        for random_index, key_2 in zip(numerical_array, sap_pad[key]['Sample_IDs']):
            sap_pad[key]['Sample_IDs'][key_2]['Pool'] = sap_pad[key]['Selected_Combo'][random_index]
    return sap_pad

def output_df(output_pad, total_number_pools):
    today = datetime.now()
    participant_list = ['Pool']
    for key in output_pad:
        participant_list.append(key)
    df = pd.DataFrame(columns = participant_list, index=range(total_number_pools))
    index = 0
    for i in range(1, total_number_pools + 1):
        df.loc[index, 'Pool'] = i
        index += 1
    for key in output_pad:
        for key_2, value_2 in output_pad[key]['Sample_IDs'].items():
            df.loc[value_2['Pool'] - 1, key] = key_2
    df.to_csv(f'pooling_strategy_{today.strftime("Date_%Y_%m_%d_Time_%H_%M_%S").replace("/","_")}.csv', index=False)

def main():
    start_time = time.time()
    directory_set_and_folder_creation()
    user_sample_list = file_identification()
    pad = pad_generator(user_sample_list)
    pool_count = pool_count_determination(pad)
    pad_selected_combo = combo_selection(pad, pool_count)
    permutation_selection(pad_selected_combo, pool_count)
    pad_pools_assigned = sample_assignment_to_pools(pad_selected_combo)
    output_df(pad_pools_assigned, pool_count)
    print(f"\n--- {(time.time() - start_time):.2f} seconds ---\n")
main()