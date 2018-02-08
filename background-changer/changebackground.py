"""
Click on image using left mouse button, grab the blue rectangle and place it
wherever in the background picture, where you want to put foreground image.
Make sure foreground image is not wider or higher than background image.
Press's' - To save the results
Press 'Esc' - To exit
"""

import cv2 as cv
import numpy as np
from tkinter import messagebox


#flags
move_rectangle = False
rect = []
BLUE = [255,0,0]    #color for rectangle

#define mouse handler
def mouse(event, x, y, flags, params):
    global move_rectangle, bg, bgCopy, rect
    #on left button down draw rectangle
    if event == cv.EVENT_LBUTTONDOWN:
        #reinitialize the image to be sure the image is clean
        bg = bgCopy.copy()
        move_rectangle = True   #change the flag
        #draw rectangle where x,y is rectangle center
        cv.rectangle(bg,(x-int(0.5*cols),y-int(0.5*rows)),
        (x+int(0.5*cols),y+int(0.5*rows)),BLUE, -1)

    elif event == cv.EVENT_MOUSEMOVE:
        if move_rectangle:
            #reinitialize the image to make sure rectangle is drawn
            #only in the position of the cursor
            bg = bgCopy.copy()
            cv.rectangle(bg,(x-int(0.5*cols),y-int(0.5*rows)),
            (x+int(0.5*cols),y+int(0.5*rows)),BLUE, -1)

    elif event == cv.EVENT_LBUTTONUP:
        if move_rectangle:
            move_rectangle = False  #stop drawing rectangle
            cv.rectangle(bg,(x-int(0.5*cols),y-int(0.5*rows)),
            (x+int(0.5*cols),y+int(0.5*rows)),BLUE, -1)
            #save rectangle coordinates for future use
            rect = [(x-int(0.5*cols)),(y-int(0.5*rows)),
            (x+int(0.5*cols)),(y+int(0.5*rows))]

def background_change(foreground, background):
    global bgCopy, bg, rows, cols, rect
    #loading images
    fg = cv.imread(foreground)
    bg = cv.imread(background)
    bgCopy = bg.copy()  # a copy of original image
    #grabing height and width of foreground image
    rows, cols = fg.shape[:2]
    #show window message
    messagebox.showinfo('Instructions',
    """Click on image and choose where you want to put foreground.
    Press Esc to exit, press S to finish the process and save.""")
    #name window
    cv.namedWindow('draw', cv.WINDOW_NORMAL)
    #resize window - need to implement deeper logic
    cv.resizeWindow('draw', int((bgCopy.shape[1])*0.5),int((bgCopy.shape[0])*0.5)
    #set mouse handler for window
    cv.setMouseCallback('draw', mouse)


    while True:

        cv.imshow('draw', bg)
        k = cv.waitKey(1)


        #waiting for esc to exit
        if k == 27 & 0xFF:
            break
        #save and begin operation on background
        elif k == ord('s'):
            #taking the coordinates choosed by user and transforming it
            roi = bgCopy[rect[1]:rect[3], rect[0]:rect[2]]

            #turning foreground into gray
            fg2gray = cv.cvtColor(fg, cv.COLOR_BGR2GRAY)
            #threshold foreground to binary
            mask = cv.threshold(fg2gray, 0.3, 255, cv.THRESH_BINARY_INV)[1]
            #bitwise conjunction of background
            bg_bitwise = cv.bitwise_and(roi, roi, mask=mask)

            #addition of images
            dst = cv.add(bg_bitwise, fg)

            #change the original fragment of background image
            #to background with applied foreground
            bgCopy[rect[1]:rect[3], rect[0]:rect[2]] = dst

            #save to file
            cv.imwrite('output.png', bgCopy)
            messagebox.showinfo('Image saved!',
            'Result saved in current directory as output.png')
            break

    # close all windows
    cv.destroyAllWindows()
