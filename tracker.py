import cv2
import numpy as np

from cell import Cell
from data_parsing import *

class Tracker:
    
    def __init__(self, left_bound, right_bound, dataparser):
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.cell = None
        self.found = False

        self.data_parser = dataparser

    def update(self, contours, frame_number):
        if contours:
            if self.found == False:
                self.cell = Cell(contours[0])
                self.found = True
                return
        else:
            return

        self.cell.update(contours[0])

        data = self.cell.get_all_calcs()

        valid_data = self.data_parser.get_valid_data(data)

        self.data_parser.add_data(valid_data, frame_number)


    def save_data(self, filename):
        self.data_parser.write_to_file(filename)
