#!/usr/bin/env python3
#
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Camera image classification demo code.

Runs continuous image classification on camera frames and prints detected object
classes.

Example:
image_classification_camera.py --num_frames 10
"""
import argparse
import contextlib
import threading

from aiy.vision.inference import CameraInference
from aiy.vision.models import image_classification
from picamera import PiCamera

from aiy.board import Board, Led

def classes_info(classes):
    return ', '.join('%s (%.2f)' % pair for pair in classes)

@contextlib.contextmanager
def CameraPreview(camera, enabled):
    if enabled:
        camera.start_preview()
    try:
        yield
    finally:
        if enabled:
            camera.stop_preview()




def main():
    parser = argparse.ArgumentParser('Image classification camera inference example.')
    parser.add_argument('--num_frames', '-n', type=int, default=None,
        help='Sets the number of frames to run for, otherwise runs forever.')
    parser.add_argument('--num_objects', '-c', type=int, default=3,
        help='Sets the number of object interences to print.')
    parser.add_argument('--nopreview', dest='preview', action='store_false', default=True,
        help='Enable camera preview')
    args = parser.parse_args()

    pressed = threading.Event()

    with PiCamera(sensor_mode=4, framerate=30) as camera, \
         CameraPreview(camera, enabled=args.preview), \
         CameraInference(image_classification.model()) as inference, \
         Board() as board:

        def on_button_released():
            pressed.clear()
            board.led.state = Led.OFF
        
        board.button.when_released = on_button_released
        while True:
            board.button.wait_for_press()
            pressed.set()
            board.led.state = Led.ON

            possibilities = {}
            while pressed.is_set():
                for result in inference.run(5):
                    classes = image_classification.get_classes(result, top_k=args.num_objects)
                    for name, probability in classes:
                        possibilities[name] = possibilities.get(name, 0) + probability
                    # print(classes_info(classes))
                    # if classes:
                    #     camera.annotate_text = '%s (%.2f)' % classes[0]
            
            best_guess = max(possibilities, key=possibilities.get)
            print(best_guess, flush=True)

if __name__ == '__main__':
    main()