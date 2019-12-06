import serial
import time
import cv2
import urllib.request
import pynmea2
import numpy as np

zoom = 16

def ecv(event, x, y, flags, param):
    global zoom
    if event == cv2.EVENT_LBUTTONDOWN:
        if (x in range(465,480) and y in range(0,20)):
            cv2.destroyWindow(winname)
            exit()
        elif (x in range(0,20) and y in range(120,140)):
             zoom = min(zoom + 1, 20)
        elif (x in range(0,20) and y in range(160,180)):
             zoom = max(zoom - 1, 1)
        

winname = "map"
cv2.namedWindow(winname)
cv2.moveWindow(winname, 0,0)
cv2.setMouseCallback(winname, ecv)
oldtime = 0
oldurl = ''
threshold = 5
baud = 9600
p = 'COM12'
ser = serial.Serial(port=p, baudrate=baud)
time.sleep(2)
        
if ser.is_open:
    while True:
        size = ser.inWaiting()
        if size:
            if time.time() - oldtime > threshold:
                oldtime = time.time()
                data = str(ser.read(size))
                data = data[2:len(data)-1]
                predata = data.split('\\r\\n')
            print(data)
            #print(predata)
            try:
                data = pynmea2.parse(predata[[i for i, s in enumerate(predata) if '$GPGGA' in s][0]])
                dataspeed = pynmea2.parse(predata[[i for i, s in enumerate(predata) if '$GPVTG' in s][0]])
                speed = dataspeed.spd_over_grnd_kmph
                if (data.latitude == 0.0 or data.longitude == 0.0): threshold = .5
                
                coordinate = str(data.latitude) + "," + str(data.longitude)
                if speed < 30: threshold = 5
                elif speed >= 30 and speed < 60: threshold = 3
                elif speed > 60: threshold = 2
                url = "https://image.maps.api.here.com/mia/1.6/mapview?app_id=<appid>&app_code=<appcode>" + coordinate + "&h=290&w=480&sb=mk&vt=0&z="+str(zoom)+"&pip&i"
                if url != oldurl:
                    oldurl = url
                    frameResp = urllib.request.urlopen(url)
                    frameNp = np.array(bytearray(frameResp.read()),dtype=np.uint8)
                    frame = cv2.imdecode(frameNp,-1)
                    cv2.line(frame,(465,5),(475,15),(0,0,255),3)
                    cv2.line(frame,(465,15),(475,5),(0,0,255),3)
                    cv2.circle(frame, (10,130), 10, (153,0,0), -1)
                    cv2.circle(frame, (10,170), 10, (153,0,0), -1)
                    cv2.putText(frame,"Speed: "+str(round(speed)),(350,10), cv2.FONT_HERSHEY_DUPLEX, .5,(0,255,0),2,cv2.LINE_AA)
                    cv2.putText(frame,"Satellite: "+str(data.num_sats),(350,30), cv2.FONT_HERSHEY_DUPLEX, .5,(0,255,0),2,cv2.LINE_AA)
                    cv2.putText(frame,"Zoom: "+str(zoom),(350,50), cv2.FONT_HERSHEY_DUPLEX, .5,(0,255,0),2,cv2.LINE_AA)
                    cv2.imshow(winname, frame)
                cv2.waitKey(10)
            #except Exception as e: print(e)
            except: pass
        #time.sleep(.3)
