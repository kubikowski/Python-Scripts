"""
Name: Twitch Bot
Written By: Nathaniel Holden
Date: 3/21/2020
Dependencies: keyboard

Inputs: a string
Outputs: writes out a string every n seconds
"""

import keyboard as kb
import asyncio


def interrupt(text):
    print(text)
    kb.write(text)


if __name__ == '__main__':
    inputStr = str(input('Enter some text: '))

    loop = asyncio.new_event_loop()
