import pandas
import numpy
import os
from tqdm import tqdm

import ExploreVisualizer

TRAIN_DIR = 'resources'
EDIT_DIR = 'resources/edited'


class DataCleaner:
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
        import csv

        largest_rows = {}
        for file in tqdm(os.listdir(directory)):
            if '.csv' in file:
                with open(directory + '/' + file, newline='') as f:
                    column_names = []
                    for row in csv.reader(f):
                        if len(row) > len(column_names):
                            column_names = row
                    largest_rows[file] = column_names
        return largest_rows

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

dc = DataCleaner()

# dc.create_train_data()
largest_rows = dc.get_max_rows(EDIT_DIR)
print(largest_rows.keys())
# print('-----')

m = 'tbi16013_Explore_v3_all_dates.csv'
compared = 'tbi16037_Explore_v3_all_dates.csv'

# diff = dc.get_diff_cols(largest_rows, m, compared)
# print("diff size: {}".format(len(diff)))
# print("main size: {}".format(len(largest_rows[m])))
# print("compared size: {}".format(len(largest_rows[compared])))

# print("check all unique: {}".format(dc.disp_cloned_cols(largest_rows, m, compared)))

# ev = ExploreVisualizer.ExploreVisualizer(largest_rows[compared])
# ev.split_cols()
# print("total: {}".format(len(largest_rows[compared])))
# print("bats: {}".format(len(ev.bats)))
# print("water: {}".format(len(ev.water)))
# print("rusty: {}".format(len(ev.rusty)))
# print("etc: {}".format(len(ev.etc)))
print('-----')
# print(ev.etc)

# dc.combine_files('Explore', 'Explore_tbi_153.csv')
# dc.combine_files('Build', 'Build_tbi_84.csv')
# dc.combine_files('Gather', 'Gather_tbi_46.csv')
# dc.combine_files('Hunt', 'Hunt_tbi_78.csv')
# dc.combine_files('Shortcut', 'Shortcut_tbi_28.csv')
# dc.combine_files('Study', 'Study_tbi_19.csv')
# dc.combine_files('Decode', 'Decode_tbi_8.csv')
# dc.combine_files('New_In-Game_Day_all_dates', 'New_In-Game_Day_all_dates_tbi_38.csv')
