import numpy as np
import cv2
import urllib.request
import pynmea2
import time

f = open("coordinate.txt","r")
winname = "map"
cv2.namedWindow(winname)
cv2.moveWindow(winname, 0,0)

while True:
        data = str(f.readline())
        data = data[:len(data)-1]
        if (data == ""): break
        predata = data.split(',')
        if (str(predata[0]) != "$GPRMC"): continue
        data = pynmea2.parse(data)
        basecoordinate = str(data.latitude) + "," + str(data.longitude)
        break

while True:
        mode = "2"
        if mode == "1":
                data = str(f.readline())
                data = data[:len(data)-1]
                if (data == ""): break
                predata = data.split(',')
                if (str(predata[0]) != "$GPRMC"): continue
                data = pynmea2.parse(data)
                coordinate = str(data.latitude) + "," + str(data.longitude)
                
                #print(coordinate)
                url = "https://image.maps.api.here.com/mia/1.6/routing?app_id=zxIpjKnVwUJHVPXF49Fz&app_code=IuikzNONXyFCodw1AaPMIQ&waypoint0=" + basecoordinate + "&waypoint1=" + coordinate + "&poix0=" + basecoordinate + ";99ff99;99ff99;0;.&poix1=" + coordinate + ";red;red;15;.&lc=3333cc&lw=6&z=16&h=290&w=480"
        elif mode == "2":
                data = str(f.readline())
                data = data[:len(data)-1]
                if (data == ""): break
                predata = data.split(',')
                if (str(predata[0]) != "$GPRMC"): continue
                data = pynmea2.parse(data)
                coordinate = str(data.latitude) + "," + str(data.longitude)
                
                #print(coordinate)
                url = "https://image.maps.api.here.com/mia/1.6/mapview?app_id=zxIpjKnVwUJHVPXF49Fz&app_code=IuikzNONXyFCodw1AaPMIQ&c=" + coordinate + "&h=290&w=480&sb=mk&vt=0&z=16&pip&i"
        else: break
        frameResp = urllib.request.urlopen(url)
        frameNp = np.array(bytearray(frameResp.read()),dtype=np.uint8)
        frame = cv2.imdecode(frameNp,-1)
        cv2.imshow(winname, frame)
        k = cv2.waitKey(10)
        if k == 27:
                break
cv2.destroyWindow(winname)
