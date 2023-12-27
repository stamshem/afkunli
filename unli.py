import time
import cv2
import ctypes
import mss
import mss.windows
import numpy as np
from ctypes import wintypes
import pyautogui
import keyboard
user32 = ctypes.windll.user32


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
            pyautogui.click(window['left']+sum_search[1][-1],window['top']+sum_search[0][-1])
        flip = cv2.matchTemplate(gray_frame, flip_png, cv2.TM_CCOEFF_NORMED)
        flip_search = np.where( flip >= 0.8)
        if len(flip_search[0]) and f!=2:
            f=2
            pyautogui.click(window['left']+flip_search[1][-1],window['top']+flip_search[0][-1],2,0.8)
        time.sleep(0.1)
t=time.time()-t        
print(i,t,i/t)
print(k,l)
