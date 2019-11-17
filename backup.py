import cv2
import time
from pyzbar import pyzbar
import requests

API_END_POINT = "http://127.0.0.1:3000/"

def sendBarcodes(barcodes):
    data = {'barcodes': barcodes}
    res = requests.post(API_END_POINT + "upload", json={"barcodes": data})
    print("Results are:: {}\n").format(res.text)

cap = cv2.VideoCapture(1)
time.sleep(2)
found = set()
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # print("{}\n").format(ret)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # decode barcodes found in the frame
    barcodes = pyzbar.decode(frame)
    print(len(barcodes))
    # Loop throught all barcodes
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        print("{}, {}").format(barcodeData, barcodeType)
        if barcodeData not in found:
            found.add(barcodeData)
            # send it to the server here
            # sendBarcodes(list(found))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()