from ppadb.client import Client
import time
import cv2
import ctypes
import mss
import mss.windows
import numpy as np
from ctypes import wintypes
import pyautogui
import keyboard
import tools
import os
from platform import system
from subprocess import check_output, Popen, PIPE


user32 = ctypes.windll.user32

cwd = os.path.dirname(__file__)
handle = user32.FindWindowW(None, 'Bluestacks App Player')
window = {} 
rect = wintypes.RECT()
user32.GetWindowRect(handle, ctypes.pointer(rect))
rect = (rect.left, rect.top, rect.right, rect.bottom)
rect = tuple(max(0, x) for x in rect)     
window['left'] = rect[0]
window['top'] = rect[1]
window['width'] = rect[2] -rect[0]
window['height'] = rect[3] -rect[1]
ctypes.windll.user32.SetForegroundWindow(handle)
awaken_png =  cv2.imread('ashem.png',cv2.IMREAD_GRAYSCALE)
cele_png = cv2.imread('bert.png',cv2.IMREAD_GRAYSCALE)
sum_png = cv2.imread('sum.png',cv2.IMREAD_GRAYSCALE)
flip_png = cv2.imread('flip.png',cv2.IMREAD_GRAYSCALE)
i=0
k,l=0,0
t=time.time()
f=False
def configureADB():
    global adb_device
    global adb_devices
    adbpath = os.path.join(cwd, 'adb.exe') # Locate adb.exe in working directory
    if system() != 'Windows' or not os.path.exists(adbpath):
        adbpath = which('adb') # If we're not on Windows or can't find adb.exe in the working directory we try and find it in the PATH
    Popen([adbpath, "kill-server"], stdout=PIPE).communicate()[0] # Restart the ADB server
    time.sleep(2)
    adb_devices = Popen([adbpath, "devices"], stdout=PIPE).communicate()[0] # Run 'adb.exe devices' and pipe output to string
    adb_device_str = str(adb_devices[26:40]) # trim the string to extract the first device
    adb_device = adb_device_str[2:15] # trim again because it's a byte object and has extra characters
    if adb_device_str[2:11] == 'localhost':
        adb_device = adb_device_str[2:16] # Extra letter needed if we manually connect
    if adb_device_str[2:10] != 'emulator' and adb_device_str[2:11] != 'localhost': # If the ADB device output doesn't use these two prefixes then:
        Popen([adbpath, 'connect', '127.0.0.1:' + str(portScan())], stdout=PIPE).communicate()[0] # Here we run portScan()
        adb_devices = Popen([adbpath, "devices"], stdout=PIPE).communicate()[0]  # Run 'adb.exe devices' and pipe output to string
        adb_device_str = str(adb_devices[26:40])  # trim the string to extract the first device
        if len(str(config.get('ADVANCED', 'port'))) > 4:
            adb_device = '127.0.0.1:' + (str(config.get('ADVANCED', 'port')))
        else:
            adb_device = adb_device_str[2:16]
def connect_device():
    global device # Contains our located device
    configureADB()
    adb = Client(host='127.0.0.1', port=5037)
    device = adb.device(adb_device) # connect to the device we extracted in configureADB()
    # PPADB can throw errors occasionally for no good reason, here we try and catch them and retry for stability
    if device == None:
        print('No ADB device found, often due to ADB errors. Please try manually connecting your client.')
    else:
        print('Device: ' + adb_device + ' successfully connected!')
        

connect_device()         
with mss.mss() as sct:
    while not keyboard.is_pressed('q'):
        frame = np.array(sct.grab(window))
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sum_ = cv2.matchTemplate(gray_frame, sum_png, cv2.TM_CCOEFF_NORMED)
        sum_search = np.where( sum_ >= 0.8)
        if len(sum_search[0]) and f!=1:
            f=1
            awaken = cv2.matchTemplate(gray_frame, awaken_png, cv2.TM_CCOEFF_NORMED)
            awaken_search = np.where( awaken >= 0.6)
            awaken_found= len(awaken_search[0])
            cele = cv2.matchTemplate(gray_frame, cele_png, cv2.TM_CCOEFF_NORMED)
            cele_search = np.where( cele >= 0.6)
            cele_found= len(cele_search[0])
            if cele_found:
                print('cele',i)
                k+=1
            if awaken_found:
                print('awaken',i)
                l+=1
            if awaken_found and cele_found:
                break
            i+=1
            device.input_tap(600,1800)
        flip = cv2.matchTemplate(gray_frame, flip_png, cv2.TM_CCOEFF_NORMED)
        flip_search = np.where( flip >= 0.8)
        if len(flip_search[0]) and f!=2:
            f=2
            device.input_tap(950,1820)
            time.sleep(0.8)
            device.input_tap(950,1820)
        time.sleep(0.1)
t=time.time()-t        
print(i,t/60/60,i/t)
print(k,l)
