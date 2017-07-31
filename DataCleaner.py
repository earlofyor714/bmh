import pandas
import numpy
import os
from tqdm import tqdm

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
                #person_data = pandas.read_csv(person_path, sep='delimiter', header=None, engine='python')
                person_data = pandas.read_csv(person_path, sep='delimiter', engine='python')
                # print(person_data)

                if training_data is not None:
                    training_data = training_data.append(person_data)
                else:
                    training_data = person_data

        print(training_data.shape)
        training_data.to_csv(EDIT_DIR + '/combined_data.csv', sep=';')

    #def combine_files(self, name):

    def get_one_line(self):
        import csv

        largest_rows = []
        for file in tqdm(os.listdir(TRAIN_DIR)):
            if '.csv' in file:
                with open(TRAIN_DIR + '/' + file, newline='') as f:
                    column_names = []
                    for row in csv.reader(f):
                        if len(row) > len(column_names):
                            column_names = row
                    print("{}: {}".format(file, len(column_names)))
                    largest_rows.append(column_names)
        print("# files: {}".format(len(largest_rows)))

            # print(row1) # type list
            # print(len(row1))

# next: want to do a diff between all the files, see how many lines in common and how many different
    # are level names shared between files?  Or is each file more/less unique?
# next: for each file, want to do a diff between all name columns
    # are they all similar?  do they expand by name?

dc = DataCleaner()
#dc.create_train_data()
dc.get_one_line()
