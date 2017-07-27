import pandas
import numpy
import os
from tqdm import tqdm

TRAIN_DIR = 'resources'

class DataCleaner:
    def __init__(self):
        self.placeholder = None

    def create_train_data(self):
        training_data = []
        for person in tqdm(os.listdir(TRAIN_DIR)):
            print(person)

    #def combine_files(self, name):


dc = DataCleaner()
dc.create_train_data()
