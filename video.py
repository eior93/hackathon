import cv

#cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
capture = cv.CaptureFromCAM(0)

def repeat():

    frame = cv.QueryFrame(capture)
    #cv.ShowImage("w1", frame)

    #cv.WaitKey(0)

    cv.SaveImage("pic.jpg", frame)

    exit(0)



while True:
    repeat()