import pandas
import numpy as np
import os
from tqdm import tqdm
import csv

# sed 1d *In-Game*.csv > edited/New_In-Game_Day_tbi_c.csv

import ExploreVisualizer

TRAIN_DIR = 'resources'
EDIT_DIR = 'resources/edited'


class CSVCombiner:
    def __init__(self):
        self.placeholder = None

    def create_train_data(self):
        training_data = None
        print("opening files")
        for person in tqdm(os.listdir(TRAIN_DIR)):
            if '.csv' in person:
                person_path = TRAIN_DIR + '/' + person
                # person_data = pandas.read_csv(person_path, sep='delimiter', header=None, engine='python')
                person_data = pandas.read_csv(person_path, sep='delimiter', engine='python')
                # print(person_data)

                if training_data is not None:
                    training_data = training_data.append(person_data)
                else:
                    training_data = person_data

        print(training_data.shape)
        training_data.to_csv(EDIT_DIR + '/combined_data.csv', sep=';')

    def combine_files(self, game_name, file_name):
        edited_path = os.path.join(EDIT_DIR, file_name)

        if os.path.isfile(edited_path):
            print("{} exists!".format(edited_path))
            return

        explore_data = open(edited_path, "a")
        explore_line_count = 0
        for raw_file in tqdm(os.listdir(TRAIN_DIR)):
            if '.csv' in raw_file and game_name in raw_file:
                full_path = os.path.join(TRAIN_DIR, raw_file)
                print(full_path)
                f = open(full_path)
                f_line_count = 0
                for line in f:
                    explore_data.write(line)
                    f_line_count += 1
                explore_line_count += f_line_count
                print("file size: {}".format(f_line_count))
                f.close()
        print("{} size: {}".format(game_name, explore_line_count))
        explore_data.close()

    def get_max_rows(self, directory):
        largest_rows = {}
        for file in tqdm(os.listdir(directory)):
            if '.csv' in file:
                with open(directory + '/' + file, newline='') as f:
                    column_names = []
                    for row in csv.reader(f):
                        if len(row) > len(column_names) and 'session_id' in row:
                            column_names = row
                    largest_rows[file] = column_names
        return largest_rows

    def remove_header_lines(self, raw_file, cleaned_file, new_header):
        edited_path = os.path.join(EDIT_DIR, cleaned_file)
        if os.path.isfile(edited_path):
            print("{} exists!".format(edited_path))
            return

        cleaned_df = pandas.DataFrame(columns=self.remove_cloned_cols(new_header))
        print("cleaned: {}".format(len(cleaned_df.columns) > len(np.unique(cleaned_df.columns))))
        print(cleaned_df.columns)

        with open(os.path.join(EDIT_DIR, raw_file), newline='') as f:
            temp_csv = pandas.DataFrame()
            temp_csv_headers = []
            line_num = 0
            for line in csv.reader(f):
                if 'session_id' in line[0]:
                    #if temp_csv.shape[0] >= 1:
                    if len(temp_csv) >= 1:
                        # convert to DataFrame, append
                        # print(temp_csv)
                        print("temp: {}".format(len(temp_csv.columns) > len(np.unique(temp_csv.columns))))
                        cleaned_df = cleaned_df.append(temp_csv)
                        line_num = 0
                    temp_csv_headers = self.remove_cloned_cols(line)
                    temp_csv = pandas.DataFrame(columns=temp_csv_headers)
                else:
                    # temp_csv.loc[line_num] = line
                    try:
                        temp_csv = temp_csv.append(pandas.Series(line, index=temp_csv_headers), ignore_index=True)
                    except ValueError:
                        print("uh oh!")
                        return
                    line_num += 1
            cleaned_df = cleaned_df.append(temp_csv)
        cleaned_df.to_csv(edited_path)

    def remove_cloned_cols(self, orig_cols):
        unique_cols = orig_cols
        ucol_num = 0
        for i, value in enumerate(unique_cols):
            for i2, subvalue in enumerate(unique_cols[i+1:]):
                if subvalue in value.split():
                    unique_cols[i + i2 + 1] += '_copy'
                elif not subvalue:
                    unique_cols[i+i2+1] = 'ucol_' + str(ucol_num)
                    ucol_num += 1
        return unique_cols

    def get_diff_cols(self, dct, main_file, compared_file):
        return list(set(dct[main_file]).intersection(dct[compared_file]))

    def check_all_unique(self, dct, main_file):
        return len(dct[main_file]) > len(set(dct[main_file]))

    def disp_cloned_cols(self, dct, main_file, compared_file):
        shared_cols = self.get_diff_cols(dct, main_file, compared_file)
        return list(set(dct[compared_file]).difference(shared_cols))


# next: want to do a diff between all the files, see how many lines in common and how many different
    # are level names shared between files?  Or is each file more/less unique?
# next: for each file, want to do a diff between all name columns
    # are they all similar?  do they expand by name?

dc = CSVCombiner()

# dc.create_train_data()
# largest_rows = dc.get_max_rows(TRAIN_DIR)
largest_rows = dc.get_max_rows(EDIT_DIR)

# person_data = pandas.read_csv(EDIT_DIR + '/Explore_tbi_153.csv', sep='delimiter', engine='python')
person_data = pandas.read_csv(TRAIN_DIR + '/tbi16012_Explore_v3_all_dates.csv', names=largest_rows['Explore_tbi_c.csv'])
print(person_data.shape[0])

# print(largest_rows.keys())
# print(len(largest_rows['Explore_tbi_153.csv']))

# dc.remove_header_lines('Explore_tbi_c.csv', 'Explore_tbi.csv', largest_rows['Explore_tbi_c.csv'])
# dc.remove_header_lines('Build_tbi_c.csv', 'Build_tbi.csv', largest_rows['Build_tbi_c.csv']) # has cloned columns
# dc.remove_header_lines('Explore_tbi_c.csv', 'Explore_tbi.csv', largest_rows['Explore_tbi_c.csv']) # DONE
# dc.remove_header_lines('Decode_tbi_c.csv', 'Decode_tbi.csv', largest_rows['Decode_tbi_c.csv']) # DONE
# dc.remove_header_lines('Gather_tbi_c.csv', 'Gather_tbi.csv', largest_rows['Gather_tbi_c.csv']) # DONE
# dc.remove_header_lines('Hunt_tbi_c.csv', 'Hunt_tbi.csv', largest_rows['Hunt_tbi_c.csv']) # DONE
# dc.remove_header_lines('New_In-Game_Day_tbi_c.csv', 'New_In-Game_Day_tbi.csv', largest_rows['New_In-Game_Day_tbi_c.csv']) # Cloned columns
# dc.remove_header_lines('Shortcut_tbi_c.csv', 'Shortcut_tbi.csv', largest_rows['Shortcut_tbi_c.csv']) # Cloned columns
# dc.remove_header_lines('Study_tbi_c.csv', 'Study_tbi.csv', largest_rows['Study_tbi_c.csv']) # DONE

# print('-----')

m = 'tbi16013_Explore_v3_all_dates.csv'
compared = 'tbi16037_Explore_v3_all_dates.csv'
compared_2 = 'tbi16012_Explore_v3_all_dates.csv'

# diff = dc.get_diff_cols(largest_rows, m, compared)
# print("diff size: {}".format(len(diff)))
# print("main size: {}".format(len(largest_rows[m])))
# print("compared size: {}".format(len(largest_rows[compared])))

# print("check all unique: {}".format(dc.disp_cloned_cols(largest_rows, m, compared)))

# ev = ExploreVisualizer.ExploreVisualizer(largest_rows[m])
# ev.split_cols()
# print("total: {}".format(len(largest_rows[m])))
# print("bats: {}".format(len(ev.bats)))
print('-----')

# dc.combine_files('Explore', 'Explore_tbi_153.csv')

# TO DO: remove rows starting with headers; add in the header at the top
