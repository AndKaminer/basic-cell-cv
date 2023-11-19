from collections import defaultdict


class DataParser:

    valid_trackers = set([
        'circ',
        'velo',
        'xpos',
        'ypos'
        ])

    to_track = set()
    collected_data = defaultdict(list)

    def __init__(self, trackable):
        if not self.check_trackable(trackable):
            raise Exception("Cannot initialize DataParser. Check the \
                    trackable setting")
        

    def check_trackable(trackable):
        for t in trackable:
            if t not in self.valid_trackers:
                return False
            else:
                self.to_track.add(t)

        return True


    def add_data(to_add: dict):
        to_update = self.to_track.copy()

        for tracked in self.to_track:
            if tracked in to_update:
                to_update.remove(tracked)

        if to_update:
            raise Exception("Necessary updates not included.")

        for tracked in self.to_track:
            if tracked in to_track:
                collected_data[tracked].append(to_add[tracked])
