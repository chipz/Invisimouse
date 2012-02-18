#!/usr/bin/python

#author @fajrhf
#email fajr.hf@gmail.com
#this is a copy of pranav mistry mouseless
#originally made by me

import cv
import Image
import win32api
import win32con
import win32gui
import time
import math

class Rect(object):
    def __init__(self):
        self.line = None
        self.wide = None
        self.center = None

#functions
def findBiggest(rects,total):
    newRects = []
    a = []
    for rect in rects:
        a.append(rect.wide)
    a.sort()
    while len(a) > total:
        a.pop(0)
    for rect in rects:
        for x in a:
            if rect.wide == x:
                newRects.append(rect)
    return newRects

def bubbleSort(fingers):
    n = len(fingers)
    while n > 1:
        newn = 0
        for i in range(0,n-1):
            if fingers[i][0] > fingers[i+1][0]:
                fingers[i],fingers[i+1] = fingers[i+1],fingers[i] #swap items
                newn = i + 1
        n = newn
    return fingers

def leftDown(finger):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,finger[0],finger[1],0,0)

def leftUp(finger):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,finger[0],finger[1],0,0)

def rightDown(finger):
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,finger[0],finger[1],0,0)

def rightUp(finger):
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,finger[0],finger[1],0,0)

#main program
if __name__ == '__main__':

    #capture pake webcam atau pake video
    capture = cv.CreateCameraCapture(1)

    #initiate part
    imageWidth = 0
    imageHeight = 0
    storage = cv.CreateMemStorage(0)
    currentFrameSize = (0,0);
    fps = 10
    camdelay = (1.0/fps)
    fixedBorder = 0
    telunjukTerangkat = False
    jariKanan = False
    jariKiri = False
    duaJari = False
    tigaJari = False
    leftFingerDown = False
    rightFingerDown = False
    finger0initX = None

    #jumlah jari yang akan dipakai
    totalJari = 3

    #karena resolusi kamera dan layar tidak sama diperlukan perbandingan
    xScale = 2 #4.26
    yScale = 2 #3.2

    counter = 0
    # definition of some colors
    _red =  (0, 0, 255, 0);
    _green =  (0, 255, 0, 0);
    _white = cv.RealScalar (255)
    _black = cv.RealScalar (0)

    t0 = time.time()

    while True:
        currentFrame = cv.QueryFrame(capture)
        currentFrameSize = (currentFrame.width, currentFrame.height)
        cvImage = cv.CreateImageHeader(currentFrameSize, cv.IPL_DEPTH_8U, 3)
        cv.SetData(cvImage, currentFrame.tostring())
        cv.ShowImage("camera", cvImage)
        if cv.WaitKey(10) == 13:
            break
    cv.DestroyWindow("camera")

    while True:
        t1 = time.time()
        #create the image to process
        currentFrame = cv.QueryFrame(capture)

        currentFrameSize = (currentFrame.width, currentFrame.height)
        
        #if there is still current frame exist
        if currentFrame:
            #make cvImage known by OpenCV
            cvImage = cv.CreateImageHeader(currentFrameSize, cv.IPL_DEPTH_8U,3)
            cv.SetData(cvImage, currentFrame.tostring())
            #flip the image on both axies
            cv.Flip(cvImage,cvImage,-1)

            #make image that'll be modified
            grayFrame = cv.CreateImage(currentFrameSize, 8, 1)
            thresholded = cv.CreateImage(currentFrameSize, 8, 1)
            gaussianed = cv.CreateImage(currentFrameSize, 8, 1)

            #converts one images space to another
            cv.CvtColor(cvImage,grayFrame,cv.CV_BGR2GRAY)
            cv.Threshold(grayFrame,thresholded,110,255,cv.CV_THRESH_BINARY)
            showGray = grayFrame
            showThresholded = thresholded


            # pre-smoothing improves Hough detector
            cv.Smooth(thresholded, gaussianed, cv.CV_GAUSSIAN, 9, 9)
            gaussian = gaussianed

            #create a storage area
            storage = cv.CreateMemStorage (0)

            #find the contours of the image
            contours = cv.FindContours(gaussianed,
                                        storage,
                                        cv.CV_RETR_TREE,
                                        cv.CV_CHAIN_APPROX_SIMPLE,
                                        (0,0))

            #create the contoured image
            contouredImage = cv.CreateImage(currentFrameSize,8,3)
            cv.SetZero(contouredImage)

            #draw the contoured image
            cv.DrawContours( contouredImage, contours,
                    _red, _green,
                    1, 1, cv.CV_AA,
                    (0,0))

            #nullified whats needed
            rects = []
            fingers = [] #untuk koordinat finger #temp

            #draw the magic!
            if len(contours) != 0:
                while contours != None:
                    rect = Rect()
                    #boxing the contours
                    rect.line = cv.BoundingRect(contours,1)

                    #calculate it's wide
                    rect.wide = math.fabs((int ( rect.line[2] - rect.line[0]) * int ( rect.line[3] -
                        rect.line[1])))

                    #find it's center
                    rect.center = (int (rect.line[0]+0.5*rect.line[2]),int
                            (rect.line[1]+0.5*rect.line[3]))

                    rects.append(rect)
                    contours = contours.h_next()

            #find biggest 4
            if len(rects) > totalJari:
                rects = findBiggest(rects,totalJari)

            for rect in rects: 
                cv.Rectangle(contouredImage, (rect.line[0],rect.line[1]),
                    (rect.line[0]+rect.line[2],rect.line[1]+rect.line[3]), cv.RGB(0,0,255))
                cv.Circle(contouredImage,
                        rect.center,
                        4,
                        cv.RGB(255,255,0),
                        1)
                #masukkan koordinat finger to fingers array
                fingers.append(rect.center)


            if fingers:
                bubbleSort(fingers)
             
            if (not fixedBorder) and len(fingers) == totalJari:
                    xJempol = fingers[0][0]
                    xTelunjuk = fingers[1][0]
                    xJariTengah = fingers[2][0]
                    antaraTengahDanTelunjuk = (xJariTengah - xTelunjuk) * 0.5 
                    fixedBorder = xTelunjuk - xJempol + antaraTengahDanTelunjuk 

            try:
                fingers[0]
            except IndexError:
                print "finger[0] not exist"
            else:
                xJempol = fingers[0][0]
                dynamicBorder = xJempol + fixedBorder 
                #gambar garis batas - dynamic border
                cv.Line(contouredImage,(int (dynamicBorder),0),(int
                    (dynamicBorder),500),cv.RGB(17, 110, 255),1,8)

            #percobaan cara baru
            #Tangible user interface
            if len(fingers) == 3:
                jariTelunjuk = fingers[1][0]
                jariTengah = fingers[2][0]
                print "duajari"

            elif len(fingers) == 2:
                jariX = fingers[1][0]
                if jariX < dynamicBorder and (leftFingerDown == False):
                    leftDown(fingers[0])
                    leftFingerDown = True
                    print "klik kiri"
                elif jariX > dynamicBorder and (rightFingerDown == False):
                    rightDown(fingers[0])
                    rightFingerDown = True
                    print "klik kanan"
            
            if (len(fingers) == 1):
                if (leftFingerDown):
                    leftUp(fingers[0])
                    leftFingerDown = False
                    print "angkat jari 1"
                    
                elif (rightFingerDown):
                    rightUp(fingers[0])
                    rightFingerDown = False
                    print "angkat jari 2"
                    
            try:
                fingers[0]
            except IndexError:
                print "fingers[0] not exist"
                initX = win32api.GetCursorPos()[0]
                initY = win32api.GetCursorPos()[1]
                print "current",win32api.GetCursorPos()
                finger0initX = None
                finger0initY = None
            else:
                if finger0initX == None:
                    finger0initX = fingers[0][0]
                    finger0initY = fingers[0][1]
                    print "dua",win32api.GetCursorPos(),"fingerinit",finger0initX,"-",finger0initY
                else:
                    try:
                        initX
                    except NameError:
                        initX = 0
                        initY = 0
                        print "tiga",win32api.GetCursorPos()
                    else:
                        resultanX = fingers[0][0] - finger0initX
                        resultanY = fingers[0][1] - finger0initY
                        print "empat",win32api.GetCursorPos(),"-resultanX",resultanX,"--resultanY",resultanY,"---",fingers[0][0],fingers[0][1]

                        x = int(xScale * resultanX + initX) 
                        y = int(yScale * resultanY + initY)
                        print "lima",x," - ",y


                        win32api.SetCursorPos((x,y)) #gerakkan mouse
                
            # after we do the MAGIC
            # create window and display the original picture in it
            cv.NamedWindow ("camera", 1)
            cv.ShowImage ("camera", cvImage)
            cv.NamedWindow("contours",1)
            cv.ShowImage("contours",contouredImage)
            #cv.ReleaseMemStorage(&storage)

            #always on top window
            windowList = []
            win32gui.EnumWindows(lambda hwnd, windowList: windowList.append((win32gui.GetWindowText(hwnd),hwnd)), windowList)
            cmdWindow = [i for i in windowList if "contours" in i[0].lower()]
            win32gui.SetWindowPos(cmdWindow[0][1],win32con.HWND_TOPMOST,0,0,currentFrame.width,currentFrame.height,0) 
            

            tn = time.time() - t1
            if tn < camdelay:
                time.sleep(camdelay-tn)
        else:
            break
        if cv.WaitKey(10) == 27:
            break
    cv.DestroyWindow("camera")
    cv.DestroyWindow("contours")
    print time.time() - t0
