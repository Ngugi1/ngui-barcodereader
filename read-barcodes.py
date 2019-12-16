# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
from pyzbar import pyzbar
from imutils.video import VideoStream
import time
import requests
import json
import serial

# v4l2-ctl -d /dev/video0 --set-ctrl=exposure_auto=1
# v4l2-ctl -d /dev/video0 --set-ctrl=focus_auto=1

def stop_motor(start=1000):
    channel = serial.Serial('/dev/ttyUSB0',9600)
    channel.write(start)

API_END_POINT = "http://52.91.230.14:3000/"
found = set()
def sendBarcodes(barcodes):
    try:
      res = requests.post(API_END_POINT + "upload", json={"barcodes": barcodes})
      print(res)
    except:
      found.remove(barcodes[0])
      print("Product not uploaded")

#sendBarcodes([5060166690144])
#exit()
def show_camera():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640) # set the Horizontal resolution
    cap.set(4, 480) # Set the Vertical resolution
    time.sleep(2)
    start = 0;
    if cap.isOpened():
        window_handle = cv2.namedWindow("BinOverflow", cv2.WINDOW_AUTOSIZE)
        # Window
        while True:
            #focus = 0  # min: 0, max: 255, increment:5
            #cap.set(28, focus);
            ret_val, frame = cap.read()
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("CSI Camera", img)
            barcodes = pyzbar.decode(img)
            for barcode in barcodes:
	       # extract the bounding box location of the barcode and draw
	       # the bounding box surrounding the barcode on the image
               (x, y, w, h) = barcode.rect
               cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
               # the barcode data is a bytes object so if we want to draw it
               # on our output image we need to convert it to a string first
               barcodeData = barcode.data.decode("utf-8")
               barcodeType = barcode.type
               # draw the barcode data and barcode type on the image
               text = "{} ({})".format(barcodeData, barcodeType)
               cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
               print(barcodeData)
               if barcodeData not in found:
                 print(barcodeData)
                 found.add(barcodeData)
                 # Tell the pi to drop the package
                 sendBarcodes([barcodeData])
                 stop_motor()
            # This also acts as
            keyCode = cv2.waitKey(30) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()
