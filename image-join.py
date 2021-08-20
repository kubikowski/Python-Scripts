"""
Name: Image Join
Written By: Nathaniel Holden
Date: 5/30/2019
Dependencies: numpy, Pillow

Inputs: a list of images
Outputs: a jpg of the images stacked horizontally or vertically
Notes: may not currently account for image directory. 
"""

import numpy as np
from PIL import Image

# This is a tool to join multiple images in an horizontal or vertical stack
# Just input the image names when requested, choose a direction, and
# choose an output name
# you don't need to add the .jpg to the input or output file names

file_names = []
while True:
    file_name: str = str(input("Image Name or (Stop): "))
    if file_name.lower() == "stop":
        break
    file_names.append(file_name + ".jpg")

images: list = [Image.open(i) for i in file_names]

# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape)
min_shape: int = sorted([(np.sum(i.size), i.size) for i in images])[0][1]

option: str = input("(h)orizontal or (v)ertical image stack? ")

if option == 'h':  # horizontal stacking
    image_matrix = np.hstack((np.asarray(i.resize(min_shape)) for i in images))
    combined_image = Image.fromarray(image_matrix)

if option == 'v':  # vertical stacking
    image_matrix = np.vstack((np.asarray(i.resize(min_shape)) for i in images))
    combined_image = Image.fromarray(image_matrix)

output_file_name = input("New Image Name: ")
combined_image.save(output_file_name + ".jpg")
