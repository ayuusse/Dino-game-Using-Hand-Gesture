import cv2
import threading
import webview
import warnings
import os
import logging
import time
import pyautogui as auto
from colorama import init, Fore , Style
from cvzone.HandTrackingModule import HandDetector
from screeninfo import get_monitors

monitors = get_monitors()
width = round((monitors[0].width-640))
height = round(monitors[0].height)

init()

detector = HandDetector(detectionCon=0.6, maxHands=1)
last_action = None
url = "https://chrome-dino-game.github.io"

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '3'
warnings.filterwarnings('ignore', category=UserWarning, module='google.protobuf')
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

def print_Msg(message, color):
    print(color + message + Fore.RESET, flush=True)

def web_cam():
    print_Msg("Starting Webcam Feed...", Fore.GREEN)                     
    video = cv2.VideoCapture(0)
    while True:
        ret,frame=video.read()
        frame = cv2.resize(frame, (640, 480))
        hands,img=detector.findHands(frame)

        if hands:
            imList=hands[0]
            fingerUp=detector.fingersUp(imList)
            if fingerUp == [0, 0, 0, 0, 0] and last_action != "space":  
                auto.press('space')
                print(f"{Fore.GREEN}Jumping...{Style.RESET_ALL}\r", end='')
                last_action = "space"
            elif fingerUp != [0, 0, 0, 0, 0]:
                last_action = None 
                print(" " * 12, end='\r')  
                
        cv2.imshow("Camera",frame)
        k=cv2.waitKey(1)
        if k==ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

def dino_game():
    print_Msg("Starting Game Feed...", Fore.LIGHTCYAN_EX)                                 
    window = webview.create_window('Dino Game', url)
    window.initial_x = 0
    window.initial_y = 0
    window.initial_width = width
    window.initial_height = height
    
    webview.start()

def run():
    print_Msg("=== Dino Game Controller Starting ===", Fore.MAGENTA)
    webcam_thread = threading.Thread(target=web_cam)
    webcam_thread.start()
    print_Msg("Thread Started...", Fore.YELLOW)    

    dino_game()

time.sleep(1)
run()
