SecuCam - Raspberry PI with Camera Module
=======

1. MDR.py  -> Motion Detection and Recording python script

This code builds on the one in Recording to a circular stream and the one in Capturing images whilst recording to demonstrate the beginnings of a security application. As before, a PiCameraCircularIO instance is used to keep the last few seconds of video recorded in memory. While the video is being recorded, video-port-based still captures are taken to provide a motion detection routine with some input (the actual motion detection algorithm is left as an exercise for the reader).

Once motion is detected, the last 10 seconds of video are written to disk, and video recording is split to another disk file to proceed until motion is no longer detected. Once motion is no longer detected, we split the recording back to the in-memory ring-buffer: