# import the necessary packages
# from pyzbar import pyzbar
# import cv2
import time
import requests

API_END_POINT = "http://52.91.230.14:3000/"

def sendBarcodes(barcodes):
    data = {'barcodes': barcodes}
    res = requests.post(API_END_POINT + "upload", json={"barcodes": data})
    print("Results are:: {}\n").format(res.text)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
# vc = cv2.VideoCapture(0)
# vs = VideoStream(usePiCamera=True).start()
time.sleep(1.0)
found = set()
# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it to
    ret, frame = vc.read()
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('frame',gray)
    # Gray frames 
    # find the barcodes in the frame and decode each of the barcodes
    # barcodes = pyzbar.decode(frame)
    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        # cv2.putText(frame, text, (x, y - 10),
                    # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # if the barcode text is currently not in our CSV file, write
        # the timestamp + barcode to disk and update the set
        if barcodeData not in found:
            print("{}\n").format(barcodeData)
            found.add(barcodeData)
            sendBarcodes(list(found))
        # show the output frame
        # cv2.imshow("Barcode Scanner", gray)
# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
# cv2.destroyAllWindows()
# vs.stop()

# Receives a list of barcodes and sends them to the server
