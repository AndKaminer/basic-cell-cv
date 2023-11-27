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
    
    dp = DataParser(settings['trackable'])

    tracker = Tracker(left, right, dp)

    data['tracker'] = tracker

    data['detector'] = Detector(data['arguments'].dtype, (0, 255, 0), 1)

    cv2.namedWindow("Video Analysis", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Video Analysis", w, h)

    return data


def edit_contours(frame, window_name):
    instance = DrawData(frame, window_name)
    print("Editing Mode On")
    cv2.setMouseCallback(window_name, draw_point, instance)
    while True:
        key = cv2.waitKey(10)
        if key == ord('e'):
            break
    
    instance.editing = False
    print("Editing Mode Off")


class DrawData:
    def __init__(self, frame, window_name):
        self.frame = frame
        self.window_name = window_name
        self.drawing = False
        self.editing = True


def get_contours_from_drawing(frame, draw_color):
    width, height, _ = frame.shape
    dest = np.zeros((width, height), np.uint8)
    mask = cv2.inRange(frame, draw_color, draw_color, dest)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours
        

def draw_point(event, x, y, flags, param):
    if not param.editing:
        return
    if event == cv2.EVENT_LBUTTONDOWN:
        param.drawing = True
    elif event == cv2.EVENT_LBUTTONUP:
        param.drawing = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if param.drawing:
            cv2.circle(param.frame, (x, y), 0, (0,255,0), -1)
            cv2.imshow(param.window_name, param.frame)


def process_key(key):
    if key == 27: # esc
        return 'BREAK'
    elif key == ord('c'):
        return 'CONTINUE'
    elif key == ord('e'):
        return 'EDIT'
    elif key == ord('s'):
        return 'CONTOUR'
    elif key == ord('r'):
        return 'RESET'
    elif key == ord('w'):
        return 'WRITE'
    else:
        return 'REDO'


def tracking_loop(data):
    contours_shown = False
    frame_num = 0

    while True:
        ret, frame = data['cap'].read()
        frame_num += 1

        print(f"Frame number: {frame_num}")
        if not ret:
            break
        
        contour_frame = frame.copy()
        backup_frame = frame.copy()
        
        data['detector'].draw_contours(contour_frame)
        _, contours = data['detector'].apply(frame)

        if not contours_shown:
            cv2.imshow("Video Analysis", frame)
        else:
            cv2.imshow("Video Analysis", contour_frame)

        while True:
            key = cv2.waitKey(0)
            action = process_key(key)
            if action == 'BREAK':
                print("Exiting")
                return
            elif action == 'CONTINUE':
                print("Continuing")
                break
            elif action == 'EDIT':
                contours_shown = False
                new_mask = edit_contours(frame, "Video Analysis")
                continue
            elif action == 'CONTOUR':
                if not contours_shown:
                    contours_shown = True
                    cv2.imshow("Video Analysis", contour_frame)
                    print("Contours Shown")
                else:
                    contours_shown = False
                    cv2.imshow("Video Analysis", frame)
                    print("Contours not shown")
            elif action == 'RESET':
                frame = backup_frame
                backup_frame = frame.copy()
                cv2.imshow("Video Analysis", frame)
                print("Clearing Canvas")
            elif action == 'WRITE':
                if contours_shown:
                    data['tracker'].update(contours)
                else:
                    new_contours = get_contours_from_drawing(frame, (0, 255, 0))
                    data['tracker'].update(new_contours)
                print("Contours written. Continuing to next slide.")
                break
            else:
                print("Invalid Char")
                continue


def main():
    data = setup()
    
    tracking_loop(data)

    data['cap'].release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
