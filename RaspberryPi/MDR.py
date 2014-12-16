#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import random
import picamera
from PIL import Image, ImageChops
import numpy as np
import datetime
import json
import requests

prior_image = None
url = \
    'https://api-m2x.att.com/v1/feeds/8170fd41e419865f2304a19098601ab0/streams/motion/value'
headers = {'Content-Type':'application/json','X-M2X-KEY': '96e4676067a781b658427c67b3c85c36'}


def postAtt(val):
    payload = {'value': str(val)}
    r = requests.put(url, data=json.dumps(payload), headers=headers)
    print r.text


def image_entropy(img):
    (w, h) = img.size
    a = np.array(img.convert('RGB')).reshape((w * h, 3))
    (h, e) = np.histogramdd(a, bins=(16, ) * 3, range=((0, 256), ) * 3)
    prob = h / np.sum(h)  # normalize
    prob = prob[prob > 0]  # remove zeros
    return -np.sum(prob * np.log2(prob))


def detect_motion(camera):
    global prior_image
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(stream)
        return False
    else:
        current_image = Image.open(stream)
        img = ImageChops.difference(current_image, prior_image)
        e = image_entropy(img)

        # Compare current_image to prior_image to detect motion. This is
        # left as an exercise for the reader!

        result = e > 0.25
        print e
        postAtt(e)

        # Once motion detection is done, make the prior image the current

        prior_image = current_image
        return result


def write_video(stream):

    # Write the entire content of the circular buffer to disk. No need to
    # lock the stream here as we're definitely not writing to it
    # simultaneously

    with io.open('before.h264', 'wb') as output:
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        while True:
            buf = stream.read1()
            if not buf:
                break
            output.write(buf)

    # Wipe the circular stream once we're done

    stream.seek(0)
    stream.truncate()


with picamera.PiCamera() as camera:
    camera.resolution = (720, 480)
    camera.annotate_frame_num = True
    camera.annotate_background = True
    camera.annotate_text = str(datetime.datetime.now())

    # camera.awb_mode='off'

    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_gains = g

    stream = picamera.PiCameraCircularIO(camera, seconds=5)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(1)
            if detect_motion(camera):
                print 'Motion detected!'

                # As soon as we detect motion, split the recording to
                # record the frames "after" motion

                camera.split_recording('after.h264')

                # Write the 10 seconds "before" motion to disk as well

                write_video(stream)

                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer

                while detect_motion(camera):
                    camera.wait_recording(1)
                print 'Motion stopped!'
                camera.split_recording(stream)
    finally:
        camera.stop_recording()

            
