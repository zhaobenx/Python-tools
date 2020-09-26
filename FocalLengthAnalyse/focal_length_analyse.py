# -*- coding: utf-8 -*-
"""
Created on 2020-09-26 13:26:26
@Author: ZHAO Lingfeng
@Version : 0.0.1
"""

import os
from collections import defaultdict

import PySimpleGUI as sg
import exifread

VERSION = '0.0.1'

SIZE_X = 200
SIZE_Y = 100

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")],
]
graph = sg.Graph(canvas_size=(400, 400),
                 graph_bottom_left=(-5, -5),
                 graph_top_right=(SIZE_X + 15, SIZE_Y + 15),
                 background_color='white',
                 key='graph')
image_viewer_column = [
    [graph],
]

layout = [[
    sg.Column(file_list_column),
    sg.VSeperator(),
    sg.Column(image_viewer_column),
]]

window = sg.Window(f'Focal Length Analyser - v{VERSION}', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        fnames = []

        for path, subdirs, files in os.walk(folder):
            for name in files:
                if name.lower().endswith((".png", ".jpg")):
                    fnames.append(os.path.join(path, name))

        window["-FILE LIST-"].update(fnames)

        focal_length = defaultdict(int)
        i = 0
        for filename in fnames:
            i += 1
            if not sg.one_line_progress_meter('Calculating', i, len(fnames), orientation='h'):
                break
            with open(filename, 'rb') as f:
                tags = exifread.process_file(f)
                focal_length[tags['EXIF FocalLength'].values[0].num] += 1

        # print(focal_length, max(focal_length))
        max_count = max(focal_length.values())
        max_focal_length = int(max(focal_length)) + 1
        min_focal_length = int(min(focal_length))
        graph.erase()

        prev_x = prev_y = None
        for fl in range(min_focal_length - 5, max_focal_length + 5):
            count = focal_length[fl]
            x = (fl - min_focal_length + 5) / (max_focal_length - min_focal_length + 5) * SIZE_X

            y = count / max_count * SIZE_Y
            if prev_x is not None:
                graph.draw_line((prev_x, prev_y), (x, y), color='red')
            if count > 0:
                graph.DrawText(text=f"({fl}mm, {count})", location=(x + 5, y + 5))
                graph.DrawPoint(
                    (x, y),
                    size=3,
                    color='blue',
                )
            prev_x, prev_y = x, y

window.close()
