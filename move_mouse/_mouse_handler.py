from math import ceil, cos, radians, sin
from time import sleep
from typing import Final

from pyautogui import MINIMUM_DURATION, moveRel, moveTo, size, Size, Point, position


class MouseHandler(object):
    def __init__(
            self: 'MouseHandler',
            movement_frequency: int = 300,
            travel_distance: int = 10,
            travel_time: float = 1.0,
    ) -> None:
        self._movement_frequency: Final[int] = movement_frequency
        self._travel_distance: Final[int] = travel_distance
        self._travel_time: Final[float] = travel_time

        self._has_value_errors()
        self._initiate_movement()

    def _has_value_errors(self: 'MouseHandler') -> None:
        if self._movement_frequency < 1:
            raise ValueError('invalid movement frequency: ({} s)'.format(self._movement_frequency))
        if self._travel_distance < 1:
            raise ValueError('invalid travel distance: ({} px)'.format(self._travel_distance))
        if self._travel_time <= MINIMUM_DURATION:
            raise ValueError('invalid travel time: ({} s)'.format(self._travel_time))
        if self._movement_frequency < self._travel_time:
            raise ValueError('movement frequency ({} s) '.format(self._movement_frequency) +
                             'must be greater than travel time ({} s)'.format(self._travel_time))

    def _initiate_movement(self: 'MouseHandler') -> None:
        while True:
            self._bind_inside_screen()
            self._move_pattern_circle()

            sleep(self._movement_frequency - self._travel_time)

    def _bind_inside_screen(self: 'MouseHandler') -> None:
        screen_size: Final[Size] = size()
        mouse_position: Final[Point] = position()

        min_x: Final[int] = min(self._travel_distance, screen_size.width // 2)
        min_y: Final[int] = min(self._travel_distance, screen_size.height // 2)

        x: Final[int] = max(min_x, min(mouse_position.x, screen_size.width - min_x))
        y: Final[int] = max(min_y, min(mouse_position.y, screen_size.height - min_y))

        if x is not mouse_position.x or y is not mouse_position.y:
            moveTo(x, y)

    def _move_pattern_diamond(self: 'MouseHandler') -> None:
        segment_travel_time: Final[float] = self._travel_time / 4

        moveRel(+self._travel_distance, +self._travel_distance, duration=segment_travel_time, _pause=False)
        moveRel(-self._travel_distance, +self._travel_distance, duration=segment_travel_time, _pause=False)
        moveRel(-self._travel_distance, -self._travel_distance, duration=segment_travel_time, _pause=False)
        moveRel(+self._travel_distance, -self._travel_distance, duration=segment_travel_time, _pause=False)

    def _move_pattern_circle(self: 'MouseHandler') -> None:
        total_segments: Final[int] = self._get_total_circle_segments()

        segment_travel_distance: Final[float] = float(self._travel_distance) * 4 / total_segments
        segment_travel_time: Final[float] = self._travel_time / total_segments

        segment_directions: Final[list[tuple[float, float]]] = []
        for segment_number in range(total_segments):
            angle_degrees: float = (360.0 / total_segments) * segment_number

            dx: float = cos(radians(angle_degrees)) * segment_travel_distance
            dy: float = sin(radians(angle_degrees)) * segment_travel_distance

            segment_directions.append((dx, dy))

        for dx, dy in segment_directions:
            moveRel(dx, dy, duration=segment_travel_time, _pause=False)

    def _get_total_circle_segments(self: 'MouseHandler') -> int:
        min_segments: Final[int] = self._travel_distance * 4
        max_segments: Final[int] = ceil(self._travel_time / MINIMUM_DURATION - 1)

        return max(min(min_segments, max_segments, 360), 1)
