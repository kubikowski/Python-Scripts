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
# you dont need to add the .jpg to the input or output file names

list_im = []
while True:
    fname = str(input( "Image Name or (Stop): " ))
    if fname.lower() == "stop": break
    list_im.append( fname + ".jpg" )

imgs = [ Image.open(i) for i in list_im ]

# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape)
min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]

option = input( "(h)orizontal or (v)ertical image stack? " )

if option == 'h': # horizontal stacking
    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
    imgs_comb = Image.fromarray( imgs_comb )

if option == 'v': # vertical stacking
    imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
    imgs_comb = Image.fromarray( imgs_comb )

outname = input( "New Image Name: " )
imgs_comb.save( outname + ".jpg" )
