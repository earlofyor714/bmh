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

        column_names = []
        with open('resources/tbi16037_Shortcut_all_dates.csv', newline='') as f:
            #for row in csv.reader(f):
            #    if len(row) > len(column_names):
            #        column_names = row
            #print(column_names)

            reader = csv.reader(f)
            row1 = next(reader)
            print(row1) # type list
            # print(len(row1))



dc = DataCleaner()
#dc.create_train_data()
dc.get_one_line()
