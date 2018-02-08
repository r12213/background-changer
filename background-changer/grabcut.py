"""
===============================================================================
Interactive Image Segmentation using GrabCut algorithm.

README FIRST:
Two windows will show up, one for input and one for output.
At first, in input window, draw a rectangle around the object using
mouse right button. Then press 'n' to segment the object (once or a few times)
For any finer touch-ups, you can press any of the keys below and draw lines on
the areas you want. Then again press 'n' for updating the output.
Key '0' - To select areas of sure background
Key '1' - To select areas of sure foreground
Key '2' - To select areas of probable background
Key '3' - To select areas of probable foreground
Key 'n' - To update the segmentation
Key 'r' - To reset the setup
Key 's' - To save the results
Key 'Esc' - To exit
===============================================================================
"""

import numpy as np
import cv2 as cv
import sys
from tkinter import messagebox

BLUE = [255,0,0]        # rectangle color
RED = [0,0,255]         # PR BG
GREEN = [0,255,0]       # PR FG
BLACK = [0,0,0]         # sure BG
WHITE = [255,255,255]   # sure FG

DRAW_BG = {'color' : BLACK, 'val' : 0}
DRAW_FG = {'color' : WHITE, 'val' : 1}
DRAW_PR_FG = {'color' : GREEN, 'val' : 3}
DRAW_PR_BG = {'color' : RED, 'val' : 2}

# setting up flags
rect = (0,0,1,1)
drawing = False         # flag for drawing curves
rectangle = False       # flag for drawing rect
rect_over = False       # flag to check if rect drawn
rect_or_mask = 100      # flag for selecting rect or mask mode
value = DRAW_FG         # drawing initialized to FG
thickness = 3           # brush thickness

def onmouse(event,x,y,flags,param):
    global img,img2,drawing,value,mask,rectangle
    global rect,rect_or_mask,ix,iy,rect_over

    # Draw Rectangle
    if event == cv.EVENT_RBUTTONDOWN:
        rectangle = True
        ix,iy = x,y

    elif event == cv.EVENT_MOUSEMOVE:
        if rectangle == True:
            img = img2.copy()
            cv.rectangle(img,(ix,iy),(x,y),BLUE,2)
            rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))
            rect_or_mask = 0

    elif event == cv.EVENT_RBUTTONUP:
        rectangle = False
        rect_over = True
        cv.rectangle(img,(ix,iy),(x,y),BLUE,2)
        rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))
        rect_or_mask = 0
        messagebox.showinfo("",
        "Now press the key 'n' a few times until no further change")

    # draw touchup curves

    if event == cv.EVENT_LBUTTONDOWN:
        if rect_over == False:
            messagebox.showwarning("","first draw rectangle")
        else:
            drawing = True
            cv.circle(img,(x,y),thickness,value['color'],-1)
            cv.circle(mask,(x,y),thickness,value['val'],-1)

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            cv.circle(img,(x,y),thickness,value['color'],-1)
            cv.circle(mask,(x,y),thickness,value['val'],-1)

    elif event == cv.EVENT_LBUTTONUP:
        if drawing == True:
            drawing = False
            cv.circle(img,(x,y),thickness,value['color'],-1)
            cv.circle(mask,(x,y),thickness,value['val'],-1)

###########################################################

def init_grab(myfile):


    global img,img2,drawing,value,mask,rectangle
    global rect,rect_or_mask,ix,iy,rect_over

    filename = myfile


    img = cv.imread(filename)
    # a copy of original image
    img2 = img.copy()
    # mask initialized to PR_BG
    mask = np.zeros(img.shape[:2],dtype = np.uint8)
    # output image to be shown
    output = np.zeros(img.shape,np.uint8)


    messagebox.showinfo("Instructions:",
    "Draw a rectangle around the object using right mouse button")
    # input and output windows
    cv.namedWindow('output')
    cv.namedWindow('input')
    cv.setMouseCallback('input',onmouse)
    cv.moveWindow('input', img.shape[1]+10,90)

    while(1):

        cv.imshow('output',output)
        cv.imshow('input',img)
        k = cv.waitKey(1)

        # key bindings
        if k == 27 & 0xFF:         # esc to exit
            break

        elif k == ord('0'): # BG drawing
            messagebox.showinfo('Pressed 0',
            "Mark background regions with left mouse button")
            value = DRAW_BG

        elif k == ord('1'): # FG drawing
            messagebox.showinfo('Pressed 1',
            "Mark foreground regions with left mouse button")
            value = DRAW_FG

        elif k == ord('2'): # PR_BG drawing
            value = DRAW_PR_BG

        elif k == ord('3'): # PR_FG drawing
            value = DRAW_PR_FG

        elif k == ord('s'): # save image
            cv.imwrite('grabcut_output.png', output)
            messagebox.showinfo('Saved',"Result saved as grabcut_output.png")
            break
        elif k == ord('r'): # reset everything
            messagebox.showinfo("Press r","resetting")
            rect = (0,0,1,1)
            drawing = False
            rectangle = False
            rect_or_mask = 100
            rect_over = False
            value = DRAW_FG
            img = img2.copy()
            # mask initialized to PR_BG
            mask = np.zeros(img.shape[:2],dtype = np.uint8)
            # output image to be shown
            output = np.zeros(img.shape,np.uint8)

        elif k == ord('n'): # segment the image
            if (rect_or_mask == 0):         # grabcut with rect
                bgdmodel = np.zeros((1,65),np.float64)
                fgdmodel = np.zeros((1,65),np.float64)
                cv.grabCut(img2,mask,rect,bgdmodel,fgdmodel,1,cv.GC_INIT_WITH_RECT)
                rect_or_mask = 1
            elif rect_or_mask == 1:         # grabcut with mask
                bgdmodel = np.zeros((1,65),np.float64)
                fgdmodel = np.zeros((1,65),np.float64)
                cv.grabCut(img2,mask,rect,bgdmodel,fgdmodel,1,cv.GC_INIT_WITH_MASK)

        mask2 = np.where((mask==1) + (mask==3),255,0).astype('uint8')
        output = cv.bitwise_and(img2,img2,mask=mask2)

    cv.destroyAllWindows()
