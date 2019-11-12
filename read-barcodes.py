# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import requests

API_END_POINT = "http://127.0.0.1:3000/"

res = requests.get(API_END_POINT + "fetch", "1")
print(res.text)


def sendBarcodes(barcodes):
    data = {'barcodes': barcodes}
    res = requests.post(API_END_POINT + "upload", json={"barcodes": data})
    print("Results are:: {}\n").format(res.text)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
args = vars(ap.parse_args())
# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(3.0)
found = set()
cv2.startWindowThread()
# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it to
    # have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)
    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # if the barcode text is currently not in our CSV file, write
        # the timestamp + barcode to disk and update the set
        if barcodeData not in found:
            print("{},{}\n").format(datetime.datetime.now(),
                                    barcodeData)
            found.add(barcodeData)
            sendBarcodes(list(found))
        # show the output frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Barcode Scanner", gray)
        key = cv2.waitKey(20)
        cv2.destroyAllWindows()
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()

# Receives a list of barcodes and sends them to the server
