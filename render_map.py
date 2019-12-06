import math
import cv2
import urllib.request
import numpy as np

resizeRatio = 1

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

def render(lat_deg, lon_deg, zoom = 16):
    global img
    listimg = []
    img = None 
    i = 0
    smurl = r"http://localhost/map/{0}/{1}/{2}.png"
    x, y = deg2num(lat_deg, lon_deg, zoom)
    xmin,xmax = x - 1, x + 1
    ymin,ymax = y - 1, y + 1
    lat_deg1, lon_deg1 = num2deg(xmin, ymin, zoom)
    disx, disy = lon_deg - lon_deg1, lat_deg1 - lat_deg

    #print(x,y,xmin,ymin,xmax,ymax)
    for xtile in range(xmin, xmax+1):
        for ytile in range(ymin, ymax+1):
            imgurl=smurl.format(zoom, xtile, ytile)
            print("Opening: " + imgurl)
            try:
                frameResp = urllib.request.urlopen(imgurl)
            except:
                print("Server is not responding")
                quit()
            
            frameNp = np.array(bytearray(frameResp.read()),dtype=np.uint8)
            if img is None:
                img = cv2.imdecode(frameNp,-1)
            else:
                img1 = cv2.imdecode(frameNp,-1)
                img = np.concatenate((img, img1), axis=0)
        listimg.append(img)
        i += 1
        img = None
    for x in range(0,i):
        if img is None:
            img = listimg[x]
        else:
            img1 = listimg[x]
            img = np.concatenate((img, img1), axis=1)

    img = cv2.resize(img,(int(img.shape[0]/resizeRatio),int(img.shape[1]/resizeRatio)))
    cv2.imshow("",img)
    

if __name__ == '__main__':
    render(51.1032097,-114.0716662, 16)
    cv2.waitKey(10)
