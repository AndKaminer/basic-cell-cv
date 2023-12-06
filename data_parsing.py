from collections import defaultdict
import os

import pandas as pd


class DataParser:

    valid_trackers = set([
        'circularity',
        'velocity',
        'xposition',
        'yposition'
        ])

    to_track = []

    def __init__(self, trackable):
        if not self.check_trackable(trackable):
            raise Exception("Cannot initialize DataParser. Check the \
                    trackable setting")

        self.collected_data = pd.DataFrame(columns=self.to_track)
        

    def check_trackable(self, trackable):
        for t in trackable:
            if t not in self.valid_trackers:
                self.to_track = []
                return False
            else:
                self.to_track.append(t)

        return True


    def get_tracked(self):
        return self.to_track


    def get_valid_data(self, data):
        try:
            new_data = { t : data[t] for t in self.to_track }
        except Exception as e:
            raise Exception(f"Data: {data} could not be made valid")
        return new_data


    def add_data(self, to_add: dict, frame_num ): # to_add is tracker -> CellDataObject
        for el in to_add.keys():
            if el not in self.to_track:
                raise Exception("Cannot add invalid column to data")

        if len(to_add.keys()) != len(self.to_track):
            raise Exception("Missing columns to add to data")

        if frame_num in self.collected_data.index:
            raise Exception("Trying to overwrite data!")

        self.collected_data.loc[frame_num] = to_add

    def write_to_file(self, filename):
        self.collected_data.to_csv(path_or_buf=filename)

    def get_dataframe(self):
        return self.collected_data
