import cv
import time

cv.NamedWindow("camera", 1)
capture = cv.CreateCameraCapture(0)

width = None
height = None
width = 320
height = 240
joss = 0

if width is None:
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)

if height is None:
    height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height)

result = cv.CreateImage((width,height),cv.IPL_DEPTH_8U,3)

def Load():

    return (faceCascade, eyeCascade)

def Display(image):
    cv.NamedWindow("Red Eye Test")
    cv.ShowImage("Red Eye Test", image)
    cv.WaitKey(0)
    cv.DestroyWindow("Red Eye Test")

def DetectRedEyes(image, faceCascade, eyeCascade):
    global joss
    min_size = (20,20)
    image_scale = 2
    haar_scale = 1.2
    min_neighbors = 2
    haar_flags = 0

    # Allocate the temporary images
    gray = cv.CreateImage((image.width, image.height), 8, 1)
    smallImage = cv.CreateImage((cv.Round(image.width / image_scale),cv.Round (image.height / image_scale)), 8 ,1)

    # Convert color input image to grayscale
    cv.CvtColor(image, gray, cv.CV_BGR2GRAY)

    # Scale input image for faster processing
    cv.Resize(gray, smallImage, cv.CV_INTER_LINEAR)

    # Equalize the histogram
    cv.EqualizeHist(smallImage, smallImage)

    # Detect the faces
    faces = cv.HaarDetectObjects(smallImage, faceCascade, cv.CreateMemStorage(0),
    haar_scale, min_neighbors, haar_flags, min_size)

    # If faces are found
    if faces:
        for ((x, y, w, h), n) in faces:
        # the input to cv.HaarDetectObjects was resized, so scale the
        # bounding box of each face and convert it to two CvPoints
            pt1 = (int(x * image_scale), int(y * image_scale))
            pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
            #cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
            face_region = cv.GetSubRect(image,(x,int(y + (h/4)),w,int(h/2)))

        cv.SetImageROI(image, (pt1[0],
            pt1[1],
            pt2[0] - pt1[0],
            int((pt2[1] - pt1[1]) * 0.7)))
        eyes = cv.HaarDetectObjects(image, eyeCascade,
        cv.CreateMemStorage(0),
        haar_scale, min_neighbors,
        haar_flags, (15,15))

        if eyes:
            # For each eye found
    #        for eye in eyes:
    #            # Draw a rectangle around the eye
    #            cv.Rectangle(image,
    #            (eye[0][0],
    #            eye[0][1]),
    #            (eye[0][0] + eye[0][2],
    #            eye[0][1] + eye[0][3]),
    #            cv.RGB(255, 0, 0), 1, 8, 0)
            kecil = 0
            for eye in eyes:
	        if kecil < eye[0][0]:
		    kecil = eye[0][0]

            for eye in eyes:
		if eye[0][0] == kecil:
		    center =  (int (eye[0][0] + eye[0][2]*0.5),int (eye[0][1] +
		        eye[0][3]*0.5))
		    cv.Circle(image,
		    center,
		    4,
		    cv.RGB(255,0,0),
                    8,
                    8,
                    1)
                    print eye
                    region = cv.GetSubRect(image,
                    (eye[0][0],
                    eye[0][1],
                    (eye[0][0] + eye[0][2]),
                    (eye[0][1] + eye[0][3])))
                    location = "data/%s.jpg" %(joss)
                    cv.SaveImage(location,region)
                    cv.SetZero(region)
                    joss = joss + 1

    cv.ResetImageROI(image)
    return image

faceCascade = cv.Load("haarcascade_frontalface_alt.xml")
eyeCascade = cv.Load("haarcascade_eye.xml")

while True:
    img = cv.QueryFrame(capture)

    image = DetectRedEyes(img, faceCascade, eyeCascade)
    cv.ShowImage("camera", image)
    k = cv.WaitKey(10);
    if k == 'f':
        break
