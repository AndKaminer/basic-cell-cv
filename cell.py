import cv2
import numpy as np

import math

TIMESTEP = .16

class Cell:
    def __init__(self, contour: np.array):
        self.contour = contour
        self.centerpoint = self.calculate_centerpoint()
        self.bounding_rect = cv2.boundingRect(contour)
        self.previous_center = None

        self.velocity_pointers = []
        self.circularity_points = []
        self.area_points = []
        self.location_points = []
        self.timesteps = []

    def calculate_centerpoint(self) -> tuple[float, float]:
        M = cv2.moments(self.contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)

    def calculate_radius(self) -> float:

        _, radius = cv2.minEnclosingCCircle(self.contour)
        return radius

    def calculate_perimeter(self) -> float:
        return cv2.arcLength(self.contour, True)

    def calculate_area(self) -> float:
        return cv2.contourArea(self.contour)

    def calculate_velocity(self) -> tuple[float, float]:
        if self.previous_center:
            curr_centerpoint = self.calculate_centerpoint()

            deltax = curr_centerpoint[0] - self.previous_center[0]
            deltay = curr_centerpoint[1] - self.previous_center[1]

            return (deltax / TIMESTEP, deltay / TIMESTEP)

        else:
            return (0, 0)

    def calculate_circularity(self):
        area = self.calculate_area()
        perimeter = self.calculate_perimeter()
        return 4 * math.pi * area / (perimeter ** 2)

    def update(self, contour):
        self.previous_center = self.calculate_centerpoint()
        self.contour = contour
        self.centerpoint = self.calculate_centerpoint()
        self.bounding_rect = cv2.boundingRect(contour)

        self.velocity_points.append(self.calculate_velocity())
        self.timesteps.append(len(self.timesteps) * TIMESTEP)
        self.circularity_points.append(self.calculate_circularity())
        self.area_points.append(self.calculate_area())
        self.location_points.append(self.calculate_centerpoint())

    def text_loc(self):
        return (self.bounding_rect[0], self.bounding_rect[1])
