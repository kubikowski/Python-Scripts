"""
Name: Twitch Bot
Author: Nathaniel Holden
Version: 0.0.1
Date: 21/03/2020
Dependencies: keyboard

Inputs:
  · a string to write out on repeat
Outputs:
  · writes out the input, as key-presses, every n seconds
"""

import asyncio

import keyboard as kb


def interrupt(text):
    print(text)
    kb.write(text)


if __name__ == '__main__':
    inputStr = str(input('Enter some text: '))

    loop = asyncio.new_event_loop()
