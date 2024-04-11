# basic-cell-cv

**THIS REPOSITORY IS DEPRECATED AND BAD DONT USE IT**

## Requirements:
 - opencv
 - python 3

## User Guide:

### Installation:
Instll opencv using pip or another package manager of choice. An environment manager like virtualenv is highly encouraged.

### Running the Tool:
The tool can be run from the command line. Two arguments need to be specified: the video file and the detector mode (for now, just use 0, since there are no other modes).
Just invoke the tool like you would a normal python command:
```
python application.py --file video.mp4 --dtype 0
```

### Usage Basics
There are two modes of operation: normal mode and editing mode.
In normal mode, there are several keys you can press. To continue to the next frame, press 'c'.
To toggle showing the program's guess on cells, press 's'.
To write whatever is on screen as data to be processed, press 'w'.
When 'w' is pressed, the program automatically skips to the next frame.
To exit the program, hit ESC.

### Editing Mode
To enter editing mode, press 'e'.
In editing mode, you can manually highlight the cells using the mouse.
Whatever is on screen when you hit 'w', be that nothing, manually highlighted cells, an edited guess, or a pure guess, is what is written as data.
To reset your drawing, hit 'r'.
To exit editing mode, press 'e' again.

### Settings
To edit settings, edit the settings.txt file.
To change the elements that are tracked, add or remove elements from the trackable setting. Do not use spaces.
