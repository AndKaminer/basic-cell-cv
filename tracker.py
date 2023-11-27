import cv2
import numpy as np

from cell import Cell

class Tracker:
    
    def __init__(self, left_bound, right_bound):
        self.num_cells: int = 0 # current number of cells on screen
        self.cell_dict: dict[int, Cell] = {} # the dictionary of cells
        self.curr_max_id: int = -1 # id of the newest cell on screen
        self.curr_min_id: int = 0 # id of the oldest cell on screen 
        self.left_bound = left_bound # left bound of the ROI
        self.right_bound = right_bound # right bound of the ROI
        self.num_old_cells = 0 # the number of old cells no tracked

    def register_cell(self, contour: np.array):
        cell = Cell(contour)
        self.cell_dict[self.curr_id + 1] = cell
        self.num_cells += 1
        self.curr_max_id += 1

    def deregister_cell(self):
        '''
        Remove the oldest cell
        '''
        if num_cells < 1:
            raise IndexError("Not enough cells in cell dictionary")
        else:
            del self.cell_dict[self.curr_min_id]
            self.curr_min_id += 1
            self.num_cells -= 1
            self.num_old_cells += 1

    def update_cell(self, cell_id: int, contour: np.array):
        if cell_id not in self.cell_dict:
            raise IndexError("Cell id not found in cell dictionary")
        else:
            self.cell_dict[cell_id].update(contour)

    def update(self, contours: list):
        if len(contours) == 0:
            return

        contours_w_centers = []

        for cnt in contours:
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            contours_w_centers.append((cnt, (cX, cY)))

        contours_w_centers.sort(key=lambda el : el[1][0])

        # count old cells
        old_cells = 0
        center = contours_w_centers[old_cells][1][0]
        while center < self.left_bound:
            old_cells += 1
            center = contours_w_centers[old_cells][1][0]

        # while more old cells in frame than recorded deregister cells
        while self.num_old_cells < old_cells:
            self.deregister_cell()
        
        # remove tracked old cells if some go off screen
        self.num_old_cells = old_cells

        # TODO - somehow detect when something leaves the screen at the same
        # as something new enters old zone
        
        # for each cell in the tracked zone, update the cell
        id = self.curr_min_id
        for i in range(old_cells, len(contours_w_centers)):
            if id > self.curr_max_id:
                break
            else:
                self.update_cell(id, contours_w_center[i][0])
                id += 1

    def show_contour_ids(self, frame):
        curr_frame = frame
        for cell_id in self.cell_dict:
            curr_frame = cv2.putText(img=curr_frame,
                                     text=str(cell_id),
                                     org=self.cell_dict[cell_id].text_loc(),
                                     fontFace=cv2.FONT_HERSHEY_PLAIN,
                                     fontScale=1,
                                     color=(0, 255, 0),
                                     thickness=1)
