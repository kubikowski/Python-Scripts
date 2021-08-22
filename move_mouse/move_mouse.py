"""
Name: Move Mouse
Author: Nathaniel Holden
Version: 0.1.2
Date: 20/08/2021
Dependencies: pyautogui

Inputs:
  · a frequency at which the mouse is moved (seconds)
Outputs:
  · moves the mouse cursor in a diamond, at a specified interval
"""

from typing import Final

from _mouse_handler import MouseHandler


def move_mouse() -> None:
    movement_frequency: Final[int] = int(input(
        'How frequently do you want the mouse to move? (seconds)\n' +
        '  · to move the mouse once every 10 minutes, enter 600\n' +
        '  · to keep the mouse moving continuously, enter 1\n' +
        '  → '
    ))

    print('press "ctrl" + "c" to stop the program')

    MouseHandler(movement_frequency)


if __name__ == '__main__':
    move_mouse()
