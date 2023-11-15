import cv2
import numpy as np

from tracker import Tracker
from cell import Cell

import argparse


def get_settings(settings_file: string):
    settings_map = {}
    with open(settings_file, 'r') as settings:
        for s in settings:
            key, val = s.split(':')
            if isnumeric(val):
                settings_map[key] = int(val)
            else:
                settings_map[key] = val

    return settings_map


def get_bounds(frame, window_x, window_y):
    cv2.namedWindow("Select Region", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Select Region", window_x, window_y)
    r = cv2.selectROI("Select Region", frame, False)

    x1, y1, width, height = r

    return (x1, x1 + width)


def get_args():
    parser = argparse.ArgumentParser(description="Cell Tracking")
    parser.add_argument('--file', dest="file")

    args = parser.parse_args()

    return args


def setup():
    """
    Returns data hashmap with:
        'settings',
        'arguments',
        'cap',
        'width',
        'height',
        'leftbound',
        'rightbound',
        'tracker'
    """
    settings = get_settings("settings.txt")
    args = get_args()

    data = {}
    data['settings'] = settings
    data['arguments'] = args

    cap = cv2.VideoCapture(args.file)
    data['cap'] = cap

    ret, frame = cap.read()

    w, h = settings['width'], settings['height']

    left, right = get_bounds(frame, w, h)

    data['width'] = w
    data['height']
    data['leftbound'] = left
    data['rightbound'] = right

    tracker = Tracker(left, right)

    data['tracker'] = tracker

    cv2.namedWindow("Video Analysis", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Video Analysis", w, h)

    return data


def tracking_loop(data):

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # TODO - implement the filtered detection stuff

        cv2.imshow("Video Analysis", frame)

        key = cv2.waitKey(20)
        if key == 27:
            break

    # TODO - return the data from the loop


def main():
    data = setup()
    
    tracking_loop()

    data['cap'].release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
