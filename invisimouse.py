#!/usr/bin/python

import cv,Image
import win32api,win32con

capture = cv.CaptureFromFile("FTIR_2_finger.avi")
imageWidth = 0
imageHeight = 0
storage = cv.CreateMemStorage(0)
currentFrameSize = (0,0);

# definition of some colors
_red =  (0, 0, 255, 0);
_green =  (0, 255, 0, 0);
_white = cv.RealScalar (255)
_black = cv.RealScalar (0)

while True:
    #create the image to process
    currentFrame = cv.QueryFrame(capture)
    #define the Width and height
    if currentFrameSize == (0,0):
        currentFrameSize = currentFrame.width,currentFrame.height
       # _currentFrameSize[1] = ,

    #print currentFrameSize

    #if there is still current frame exist
    if currentFrame:
        #make cvImage known by OpenCV
        #cvImage = cv.CreateImageHeader(currentFrameSize, cv.IPL_DEPTH_8U, 3)
        #cv.SetData(cvImage, currentFrame)
        #currentFrame = Image.open("stupid.jpg")
        cvImage = cv.CreateImageHeader(currentFrameSize, cv.IPL_DEPTH_8U,3)
        cv.SetData(cvImage, currentFrame.tostring())

        #make image that'll be modified
        grayFrame = cv.CreateImage(currentFrameSize, 8, 1)
        thresholded = cv.CreateImage(currentFrameSize, 8, 1)
        cv.CvtColor(cvImage,grayFrame,cv.CV_BGR2GRAY)
        cv.Threshold(grayFrame,thresholded,60,255,cv.CV_THRESH_BINARY)


        # pre-smoothing improves Hough detector
        cv.Smooth(thresholded, grayFrame, cv.CV_GAUSSIAN, 9, 9)

        #create a storage area
        storage = cv.CreateMemStorage (0)

        #find the contours of the image
        #print "tipeimej",type(thresholded)
        contours = cv.FindContours(thresholded,
                                    storage,
                                    cv.CV_RETR_TREE,
                                    cv.CV_CHAIN_APPROX_SIMPLE,
                                    (0,0))

        if len(contours) != 0:
        # comment this out if you do not want approximation
            print "tipecontours",type(contours)
            print contours
            contourse = cv.ApproxPoly (contours,
                                        storage,
                                        cv.CV_POLY_APPROX_DP,3,1)
        #create the contoured image
        contouredImage = cv.CreateImage(currentFrameSize,8,3)
        cv.SetZero(contouredImage)

        # initialisation
        _contours = contours
        print "_contours type",type(_contours)

        #draw the contoured image
        cv.DrawContours( contouredImage, _contours,
                _red, _green,
                1, 1, cv.CV_AA,
                (0,0))

        loop = len(_contours)
        print "pjg loop",loop
        currentLoop = 0
        #draw the magic!
        if len(_contours) != 0:
            while _contours != None:
                print "contours now",len(_contours)
                insideLoop = 0
                for rect in _contours:
                    print rect
                    print "rect",type(rect)
                    cv.Circle(contouredImage,rect,4,_green,1)
                    myRect = cv.BoundingRect(_contours,1)
                    #print "myRect", myRect
                    center = (int (myRect[0]+0.5*myRect[2]),int (myRect[1]+0.5*myRect[3]))
                    cv.Rectangle(contouredImage, (myRect[0],myRect[1]),
                        (myRect[0]+myRect[2],myRect[1]+myRect[3]), cv.RGB(0,0,255))
                    cv.Circle(contouredImage,
                            center,
                            4,
                            cv.RGB(255,255,0),
                            1)
                    win32api.SetCursorPos(center)
                    insideLoop = insideLoop + 1
                    print "insideLoop =",insideLoop
                _contours = _contours.h_next()
                currentLoop = currentLoop + 1
                print "currentLoop =",currentLoop

        print "this"
        # after we do the MAGIC
        # create window and display the original picture in it
        cv.NamedWindow ("camera", 1)
        cv.ShowImage ("camera", cvImage)
        cv.NamedWindow("contours",1)
        cv.ShowImage("contours",contouredImage)
        #cv.ReleaseMemStorage(&storage)
    else:
        break
    if cv.WaitKey(10) == 27:
        break
#cv.ReleaseCapture( &currentFrame )
cv.DestroyWindow("camera")
cv.DestroyWindow("contours")
