import cv2
import numpy as np

class Detector:

    def __init__(self, detector_type, drawing_color, drawing_thickness):
        if detector_type == 0:
            self.detector = cv2.createBackgroundSubtractorMOG2()
        else:
            self.detector = cv2.createBackgroundSubtractorMOG2()
            # TODO - add other detector types

        if (len(drawing_color) != 3 or drawing_color[0] not in range(0, 256) or
            drawing_color[1] not in range(0, 256) or drawing_color[2] not in range(0, 256)):
            raise Exception("Invalid color")

        self.drawing_color = drawing_color
        self.drawing_thickness = drawing_thickness

        
    def apply(self, frame):
        mask = self.detector.apply(frame)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return mask, contours


    def draw_contours(self, frame):
        mask, contours = self.apply(frame)
        cv2.drawContours(frame, contours, -1, self.drawing_color,
                         self.drawing_thickness)


    def draw_bounding_rects(self, frame):
        mask, contours = self.apply(frame)
        for c in contours:
            rect = cv2.boundingRect(c)
            cv2.rectangle(frame, (int(rect[0]), int(rect[1])),
                          (int(rect[0] + rect[2]), int(rect[1] + rect[3])),
                          (0,255,0), 1)
    
    
    def draw_contour_outline(self, frame):
        kernel = np.ones((3, 3), np.uint8)

        mask, contours = self.apply(frame)
        dilation = cv2.dilate(mask, kernel, iterations=1)
        outline = cv2.bitwise_xor(mask, dilation)
        new_contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, new_contours, -1, self.drawing_color, self.drawing_thickness)
