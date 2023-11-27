from collections import defaultdict


class DataParser:

    valid_trackers = set([
        'circ',
        'velo',
        'xpos',
        'ypos'
        ])

    to_track = set()
    collected_data = {}

    def __init__(self, trackable):
        if not self.check_trackable(trackable):
            raise Exception("Cannot initialize DataParser. Check the \
                    trackable setting")

        for el in self.to_track:
            self.collected_data[el] = SingleAttributeParser()
        

    def check_trackable(self, trackable):
        for t in trackable:
            if t not in self.valid_trackers:
                return False
            else:
                self.to_track.add(t)

        return True


    def add_data(self, to_add: dict): # to_add is tracker -> CellDataObject
        for el in to_add.keys():
            if not el in self.to_track:
                raise Exception("Invalid tracker")

            self.collected_data[el].add_data(to_add[el])


class SingleAttributeParser:

    def __init__(self):
        self.data = defaultdict(list) # id -> [(time, dp), ...]

    def add_data(self, data_object):
        for key in data_object.get_data():
            self.data[key].append(data_object.get_data()[key])

    def get_chart_objects(self, id):
        if id not in self.data:
            raise Exception("Invalid id")

        timesteplist = []
        valuelist = []

        for time, dp in self.data[id]:
            timesteplist.append(time)
            valuelist.append(dp)


class CellDataObject:

    def __init__(self):
        self.id_to_dp = {} # cell_id -> (time, dp)

    def add_datapoint(self, id, time, value):
        self.id_to_dp[id] = (time, value)

    def get_data(self):
        return self.id_to_dp
