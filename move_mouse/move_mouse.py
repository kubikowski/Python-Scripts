"""
Name: Move Mouse
Author: Nathaniel Holden
Version: 0.1.1
Date: 20/08/2021
Dependencies: pyautogui

Inputs:
  · a frequency at which the mouse is moved (seconds)
Outputs:
  · moves the mouse cursor in a diamond, at a specified interval
"""

from time import sleep
from typing import Final

from pyautogui import moveRel, moveTo, size, Size, Point, position


def move_mouse() -> None:
    frequency: int = int(input(
        'How frequently do you want the mouse to move? (seconds)\n' +
        '  · to move the mouse once every 10 minutes, enter 600\n' +
        '  · to keep the mouse moving continuously, enter 1\n' +
        '  → '
    ))

    print('press "ctrl" + "c" to stop the program')

    move_mouse_loop(frequency)


def move_mouse_loop(frequency: int = 300, distance: int = 5) -> None:
    if frequency < 1:
        raise ValueError('invalid frequency: "{}"'.format(frequency))
    if distance < 1:
        raise ValueError('invalid distance: "{}"'.format(distance))

    while True:
        _bind_mouse_position(distance)
        _move_mouse_diamond(distance)

        sleep(frequency - 1)


def _bind_mouse_position(distance: int) -> None:
    screen_size: Final[Size] = size()
    mouse_position: Final[Point] = position()

    min_x: Final[int] = min(2 * distance, screen_size.width // 2)
    min_y: Final[int] = min(2 * distance, screen_size.height // 2)

    x: Final[int] = max(min_x, min(mouse_position.x, screen_size.width - min_x))
    y: Final[int] = max(min_y, min(mouse_position.y, screen_size.height - min_y))

    if x is not mouse_position.x or y is not mouse_position.y:
        moveTo(x, y)


def _move_mouse_diamond(distance: int) -> None:
    moveRel(+distance, +distance, 0.25)
    moveRel(-distance, +distance, 0.25)
    moveRel(-distance, -distance, 0.25)
    moveRel(+distance, -distance, 0.25)


if __name__ == '__main__':
    move_mouse()
