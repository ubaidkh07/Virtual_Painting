import cv2
import matplotlib.pyplot as plt
import HandTrackingModule as htm
import mediapipe as mp
import numpy as np


detector=htm.handDetector()
draw_color=(255,0,0)
#creating img canvas
img_canvas=np.zeros((720,1280,3),np.uint8)   #rgb=3 , binary=none

cap=cv2.VideoCapture(0)

while True:
    success,img=cap.read()
    img=cv2.resize(img,(1280,720))
    img=cv2.flip(img,1)
	
    rect=cv2.rectangle(img,pt1=(10,30),pt2=(250,100),color=(255,0,0),thickness=-1)
    rect=cv2.rectangle(img,pt1=(260,30),pt2=(500,100),color=(0,255,0),thickness=-1)
    rect=cv2.rectangle(img,pt1=(510,30),pt2=(750,100),color=(0,0,255),thickness=-1)
    rect=cv2.rectangle(img,pt1=(760,30),pt2=(1000,100),color=(255,255,0),thickness=-1)
    rect=cv2.rectangle(img,pt1=(1010,30),pt2=(1270,100),color=(255,255,255),thickness=-1)
    text=cv2.putText(img,text='ERASER',org=(1038,76),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=1,color=(0,0,0),thickness=3)

    #detect hands
    img=detector.findhands(img)
    lmlist=detector.findPosition(img)
    #print(lmlist)

    if len(lmlist)!=0:
        x1,y1=lmlist[8][1:] #index finger tip coordinates
        x2,y2=lmlist[12][1:] #middle finger tip coordinates

    #detect finger areup
        fingers=detector.fingersUp()
        print(fingers) 

    #check if two fingers are up = selection mode
        if fingers[1] and fingers[2]:
            print("selection mode" )
            xp,yp=0,0
	
            if(y1<100):

	            if 10<= x1 <=250:
	                print("red")
                    draw_color=(255,0,0)	
                elif 260<= x1 <=500:
	                print("green")
                    draw_color=(0,255,0)
                elif 510 <=x1<=750:
                    print("blue")
		            draw_color=(0,0,255)
	            elif  760<=x1<=1000:
                    print("yellow")
		            draw_color=(255,255,0)
	            elif 1010 <=x1<=1270:
                    print("Eraser")
		            draw_color=(0,0,0)

	        cv2.rectangle(img,(x1,y1),(x2,y2),color=draw_color,thickness=-1)

#check if index finger = drawing mode(one finger)
      if (fingers[1] and not fingers[2]):

	        cv2.circle(img,(x1,y1),15,draw_color,thickness=-1)
	        print("drawing mode")
	        if xp==0 and yp==0:
	            xp=x1
	            yp=y1		
	#colors
	      if draw_color==(0,0,0):
	        cv2.line(img,(xp,yp),(x1,y1),color=draw_color,thickness=50)
	        cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=50)

	     else:
	        cv2.line(img,(xp,yp),(x1,y1),color=draw_color,thickness=15)
	        cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=15)

	        xp,yp=x1,y1
	#merging		
	img_grey=cv2.cvtColor(img_canvas,cv2.COLOR_BAYER_BG2BGRAY)
	_,img_inverse=cv2.threshold(img_grey,20,255,cv2.THRESH_BINARY_INV)
	img_inverse=cv2.cvtColor(img_inverse,cv2.COLOR_GRAY2BGR)
    
    img=cv2.bitwise_and(img,img_inverse)
	img=cv2.bitwise_or(img,img_canvas)
	
    img=cv2.addWeighted(img,1,img_canvas,0.5,0)


    cv2.imshow('virtual painter',img)
    if cv2.waitKey(1) & 0XFF==27:
        break
cap.release()
cv2.destroyAllWindows()
