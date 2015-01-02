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
import math,operator

prior_image = None
url = \
    'https://api-m2x.att.com/v1/feeds/key/streams/motion/value'
headers = {'Content-Type':'application/json','X-M2X-KEY': 'key'}
filenum=0

def postAtt(val):
    payload = {'value': str(val)}
    try:
        r = requests.put(url, data=json.dumps(payload), headers=headers)
        #print r.text
    except:
        print ('Error posting data')
        pass


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
    camera.capture(stream, format='jpeg', use_video_port=True,resize=(320,240))
    stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(stream)
        return False
    else:
        current_image = Image.open(stream)
        img = ImageChops.difference(current_image, prior_image)

        #h1 = prior_image.histogram()
        #h2 = current_image.histogram()
        
        #e = math.sqrt(reduce(operator.add, map(lambda a,b: (a-b)**2, h1, h2))/len(h1))

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
    global filenum
    # Write the entire content of the circular buffer to disk. No need to
    # lock the stream here as we're definitely not writing to it
    # simultaneously

    with io.open('upload/' + str(filenum) + '-before.h264', 'wb') as output:
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        while True:
            buf = stream.read1()
            if not buf:
                break
            output.write(buf)
            filenum += 1

    # Wipe the circular stream once we're done

    stream.seek(0)
    stream.truncate()


with picamera.PiCamera() as camera:
    camera.resolution = (720, 480)
    camera.annotate_frame_num = True
    camera.annotate_background = True
    camera.annotate_text = str(datetime.datetime.now())

    # camera.awb_mode='off'
    camera.framerate=15
    #camera.exposure_mode = 'off'
    #g = camera.awb_gains
    #camera.awb_gains = g

    stream = picamera.PiCameraCircularIO(camera, seconds=5)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(2)
            if detect_motion(camera):
                print 'Motion detected!'

                # As soon as we detect motion, split the recording to
                # record the frames "after" motion

                camera.split_recording('upload/' + str(filenum) + '-after.h264')

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
