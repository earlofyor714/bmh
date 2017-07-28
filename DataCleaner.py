import pandas
import numpy
import os
from tqdm import tqdm

TRAIN_DIR = 'resources'

class DataCleaner:
    def __init__(self):
        self.placeholder = None

    def create_train_data(self):
        training_data = None
        print("opening files")
        for person in tqdm(os.listdir(TRAIN_DIR)):
            person_path = TRAIN_DIR + '/' + person
            #person_data = pandas.read_csv(person_path, sep='delimiter', header=None, engine='python')
            person_data = pandas.read_csv(person_path, sep='delimiter', engine='python')
            # print(person_data)

            if training_data is not None:
                training_data = training_data.append(person_data)
            else:
                training_data = person_data

        print(training_data.shape)

    #def combine_files(self, name):


dc = DataCleaner()
dc.create_train_data()
