# -*- coding: utf-8 -*-
"""
Created on 2019-04-22 22:32:32
@Author: ZHAO Lingfeng
@Version : 0.0.1
"""
import os
import sys
import logging

if os.environ.get('debug'):
    logging.basicConfig(filename='debug.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',level=logging.DEBUG)

def log(text):
    logging.info(text)


import PySimpleGUI as sg
from PIL import Image

try:
    import distutils
    log("Import distutils success")
except Exception as e:
    log(f"Import error {e}")

try:
   wd = sys._MEIPASS
except AttributeError:
   wd = os.getcwd()
icon_file = os.path.join(wd,'resource/icon.ico')

def concatenate_image(image_list, output_name, progress_bar_callback=None, progress_text_callback=None):
    def update_text(text):
        if progress_text_callback:
            progress_text_callback(text)

    def update_progress_bar(i, all):
        if progress_bar_callback:
            progress_bar_callback(i, all)

    images = []
    image_names = []
    for i in image_list:
        try:
            image = Image.open(i)

        except Exception as e:
            update_text(f"Failed on reading {i}: {e}")
            log(f"Failed on reading {i}: {e}")
        else:
            images.append(image)
            image_names.append(os.path.basename(i))
            update_text(f"Open image {i}")
            log(f"Open image {i}")

    image_number = len(images)
    if image_number == 0:
        update_text("No images")
        return

    width = min([i.size[0] for i in images])
    length = 0
    # update_text("Stitching")
    for i in images:
        length += int(width / i.size[0] * i.size[1])

    result = Image.new('RGB', (width, length))

    length_i = 0
    for index, i in enumerate(images):
        update_text(f"Stithing {image_names[index]}")
        update_progress_bar(index + 1, image_number)
        w, h = i.size
        h_ = int(width / w * h)
        result.paste(i.resize((width, h_)), (0, length_i))
        length_i += h_

    update_text('Saving')
    log("Stitch done")
    result.save(output_name)
    update_text('Done')


def main():
    log("program starts")
    layout = [[sg.Text('Select photos to concatenate')],
              [
                  sg.Text('Source images'),
                  sg.Input(),
                  sg.FilesBrowse(file_types=(("Image Files", "*.jpg;*.png;*.jpeg;*.bmp;*.tiff"), ))
              ], [sg.Text('Output image'), sg.Input('result.jpg', )],
              [
                  sg.ProgressBar(1000, orientation='h', size=(40, 20), key='progbar'),
                  sg.Text('', key='progtext', size=(20, 1))
              ], [
                  sg.Submit('Start'),
                  sg.Cancel(),
              ]]

    window = sg.Window('Image concatenate',icon=icon_file).Layout(layout)

    while True:
        _, files = window.Read()
        if _ == 'Cancel' or _ is None:
            log("Cancel")
            window.Close()
            sys.exit(0)

        if not files[0]:
            log("No file")
            sg.Popup("Please select image")
            continue

        source_images = files[0].split(';')
        output_image = files[1]
        log(f"Source images: {source_images}")
        log(f"Output images: {output_image}")
        print(source_images, output_image)
        concatenate_image(source_images, output_image,
                          window.FindElement('progbar').UpdateBar,
                          window.FindElement('progtext').Update)
        sg.Popup('Done')

    window.Close()


if __name__ == "__main__":
    main()