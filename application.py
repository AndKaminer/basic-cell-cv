import cv2
import numpy as np

from tracker import Tracker
from cell import Cell
from data_parsing import DataParser
from detector import Detector

import argparse
import os


def get_settings(settings_file: str):
    settings_map = {}
    with open(settings_file, 'r') as settings:
        for s in settings:
            key, val = s.split(':')
            val = val[:-1]
            if val.isnumeric():
                settings_map[key] = int(val)
            elif ',' in val:
                settings_map[key] = val.split(',')
            else:
                settings_map[key] = val

    return settings_map


def get_bounds(frame, window_x, window_y):
    cv2.namedWindow("Select Region", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Select Region", window_x, window_y)
    r = cv2.selectROI("Select Region", frame, False)
    cv2.destroyWindow("Select Region")

    x1, y1, width, height = r

    return (x1, x1 + width)


def get_args():
    parser = argparse.ArgumentParser(description="Cell Tracking")
    parser.add_argument('--file', dest="file")
    parser.add_argument('--dtype', dest="dtype")

    args = parser.parse_args()

    if not args.file:
        raise Exception("Please specify a file")
    elif not os.path.exists(args.file):
        raise Exception("File does not exist. Please specify a valid path")
    elif not args.file.endswith(('.mp4', '.cine', '.avi')):
        raise Exception("File is not of valid format. Please specify a file of \
                type mp4, cine, or avi")

    if not args.dtype:
        raise Exception("Please specify a detector type")

    args.dtype = int(args.dtype)

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
        'tracker',
        'detector'
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
    data['height'] = h
    data['leftbound'] = left
    data['rightbound'] = right

    tracker = Tracker(left, right)

    data['tracker'] = tracker
    data['dataParser'] = DataParser(settings['trackable'])

    data['detector'] = Detector(data['arguments'].dtype, (0, 255, 0), 2)

    cv2.namedWindow("Video Analysis", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Video Analysis", w, h)

    return data


def tracking_loop(data):

    while True:
        ret, frame = data['cap'].read()

        if not ret:
            break

        data['detector'].draw_bounding_rects(frame)

        cv2.imshow("Video Analysis", frame)

        key = cv2.waitKey(20)
        if key == 27:
            break


def main():
    data = setup()
    
    tracking_loop(data)

    data['cap'].release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
