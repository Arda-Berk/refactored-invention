import os
import cv2
import time
import win32ui
import win32api
import win32con
import win32gui
import numpy as np
from skimage import io

#https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows
def get_screenshot(mappath, scope):
    x0, y0 = win32api.GetCursorPos()
    wDC = win32gui.GetWindowDC(None)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, int(120*scope), int(120*scope))
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0),(int(120*scope), int(120*scope)) , dcObj, (int(x0-(60*scope)), int(y0-(60*scope))), win32con.SRCCOPY)  #0, 0, w, h, x, y
    dataBitMap.SaveBitmapFile(cDC, mappath)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(None, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

def get_players(mappath, scope):
    x0, y0 = win32api.GetCursorPos()
    image = io.imread(mappath) #use cv2.imread in case this doesn't work
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0) #this might need calibration
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            win32api.SetCursorPos((int(x0+x-(60*scope)),int(y0+y-(60*scope))))

scope = 1

ScopeMode = 2

FPS = 0

exceptions = []
 
dir_path = os.path.dirname(os.path.realpath(__file__))

mappath = dir_path + "\image.bmp"

#https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes

print("""
                                                  AimBot 2.5
                                                                                                               """)
print("\n>>>Eğer imleciniz hedefinizin yakınındaysa LSHIFT tuşuna basarak hedefinizi düzeltebilirsiniz.")
print("\n>>>Bot, sizin için otomatik ateş etmeyecektir, o yüzden hedefinizi düzeltirken sol tık yapmayı unutmayın.")
print("\n>>>Sayısal tuş takımındaki '2', '4' ve '8' rakamlarına basarak dürbününüzü ayarlayabilirsiniz.")
print("\n>>>CTRL + T ile hataları error_logs.txt'e kaydederek botu kapatabilirsiniz.")
print("\n>>>Hesabınız ban yerse bundan siz sorumlusunuz.")
input("\n>>>Devam etmek istiyorsanız Enter tuşuna basın.")
print("\n>>>Artık bu ekranı simge durumunda küçültüp oyununuzu normal bir şekilde oynayabilirsiniz.\n")       
while True:
    try:
        if win32api.GetAsyncKeyState(0x10) < 0:
            start_time = time.time()
            get_screenshot(mappath, scope)
            get_players(mappath, scope)  
            FPS = format(round((1.0/(time.time() - start_time)), 2), '.2f')
            print("\r>>>Bot: Çalışıyor. Dürbün modu: {} FPS: {}                                                                  ".format(ScopeMode, FPS), end='')
        if win32api.GetAsyncKeyState(0x62) < 0: 
            scope = 1
            ScopeMode = 2
        if win32api.GetAsyncKeyState(0x64) < 0: 
            scope = 0.75
            ScopeMode = 4
        if win32api.GetAsyncKeyState(0x68) < 0:
            scope = 0.5
            ScopeMode = 8
        if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x54) < 0:
            errorlogs = dir_path + "\error_logs.txt"
            f = open(errorlogs, "w")
            for exception in exceptions:
                f.write(str(exception) + "\n")
            f.close()
            print("\n")
            quit()
        else:       
            print("\r>>>Bot: Beklemede. Dürbün modu: {} FPS: {}                                                                  ".format(ScopeMode, FPS), end='')
    except Exception as e:
        print("\r>>>Bot hâlâ çalışıyor ama bir hatayla karşılaştı: {}".format(e), end='')
        if str(e) not in exceptions:
            exceptions.append(str(e))
        pass
