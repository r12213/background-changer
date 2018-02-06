# Background Changer

Simple python based app that uses opencv library.

## Description
Basic tool which allows you to load image,
segment image using grabcut algorithm, extract specific object from picture.
After image segmentation, you can put your segmented image on any background.

### Prerequisites
Module                                                     | Version
-------                                                    |--------
[opencv-python](https://pypi.python.org/pypi/opencv-python)|_3.4.0.12_
[numpy](http://www.numpy.org/)                             |_1.13.3_

### Installation
    git clone https://github.com/r12213/background-changer.git
    cd background-changer
    pip install opencv-python
    pip install numpy


### Running program
Run ``main.py``
Steps:
1. Load image you want to segment/extract object e.g. face.
2. Load image you wish to be background of segmented image.
3. Apply GrabCut on first image a.k.a "foreground image"
with "GrabCut" dropdown menu.
4. Put extracted foreground image on loaded background image
with "Change Back" dropdown menu.

Result is saved as output.png in current working directory.    

### Sample outputs
<img align="left" height="320" src="https://i.imgur.com/aSk4wYB.jpg"/>
<img align="right" height="320" src="https://i.imgur.com/F4aMHxn.jpg"/>

<img align="left" height="320" src="https://i.imgur.com/LpYqSgg.jpg"/>
<img align="right" height="320" src="https://i.imgur.com/0DWhUVO.jpg"/>


### Todos

 - resize window in Change Back tool to full screen
 - replace blue rectangle in Change Back tool with actual image
 - add some resize method for foreground pictures wider or higher than new background
 - deal with case, when rectangle is beyond the background dimensions
