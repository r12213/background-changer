#!/usr/bin/env python
"""
===============================================================================
Background changer

Basic tool which allows you to load image,
segment image using grabcut algorithm, extract specific object from picture.
After image segmentation, you can put your segmented image on any background.

Steps:
1. Load image you want to segment/extract object e.g. face.
2. Load image you wish to be background of segmented image.
3. Apply GrabCut on first image a.k.a "foreground image"
with "GrabCut" dropdown menu.
4. Put extracted foreground image on loaded background image
with "Change Back" dropdown menu.

Result is saved as output.png in current working directory.

===============================================================================
"""

from tkinter import Frame, Tk, BOTH, Text, Menu, END
from tkinter import filedialog, messagebox
import os
import grabcut
import changebackground


# flags
fg_loaded = False
bg_loaded = False


class Base(Frame):

    text_initialized = False

    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):

        self.master.title("Background changer")
        self.pack(fill=BOTH, expand=1)
        # create menu
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # add menu widgets
        file_menu = Menu(menubar)
        grabcut_menu = Menu(menubar)
        change_menu = Menu(menubar)

        # add file menu object
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load foreground image",
                              command=self.on_open_fg)
        file_menu.add_command(label="Load background image",
                              command=self.on_open_bg)

        # add menu object but only if image for method is loaded
        if fg_loaded:
            menubar.add_cascade(label="GrabCut", menu=grabcut_menu)
            # add command depend on flag (e.g. image_loaded = True)

            grabcut_menu.add_command(label='Extract object from image',
                                     command=self.on_grab)

        if bg_loaded and os.path.exists('grabcut_output.png'):
            menubar.add_cascade(label="Change Back", menu=change_menu)
            change_menu.add_command(label="Apply extracted foreground\
 image on loaded background image", command=self.on_background)

    def on_open_fg(self):

        global fg_loaded, image_fg_path

        ftypes = [('JPG files', '*.jpg'), ('PNG files', '*.png'),
                  ('All files', '*')]
        dlg = filedialog.Open(self, title="Select image file",
                              filetypes=ftypes)

        image_fg_path = dlg.show()
        # make sure user loaded something
        if len(image_fg_path) > 0:
            fg_loaded = True
            messagebox.showinfo("Success!", "Foreground image loaded\
 successfully! You can now use use image segmentation with Grabcut!")
            # initialize again to access grabcut
            self.initialize()

    def on_open_bg(self):

        global bg_loaded, image_bg_path

        ftypes = [('JPG files', '*.jpg'), ('PNG files', '*.png'),
                  ('All files', '*')]
        dlg = filedialog.Open(self, title="Select image file",
                              filetypes=ftypes)

        image_bg_path = dlg.show()
        # make sure user loaded something
        if len(image_bg_path) > 0:
            bg_loaded = True
            messagebox.showinfo("Success",
                                "Background image loaded successfully")
            # initialize again to access background menu
            self.initialize()

    def on_grab(self):
        self.display_text(grabcut.__doc__)
        # init grabcut
        grabcut.init_grab(image_fg_path)
        self.txt.forget()
        Base.text_initialized = False
        # initialize again to access background menu
        self.initialize()

    def display_text(self, text):
        if not Base.text_initialized:
            # first create text
            self.txt = Text(self)
            self.txt.pack(fill=BOTH, expand=1)
            self.txt.insert(END, text)
            Base.text_initialized = True

    def on_background(self):
        self.display_text(changebackground.__doc__)
        ###
        changebackground.background_change('grabcut_output.png', image_bg_path)
        self.txt.forget()
        Base.text_initialized = False


def main():

    root = Tk()
    run = Base()
    root.geometry("700x450+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()
