from datetime import datetime
import cv2 ,pandas
video = cv2.VideoCapture(0) # which camera to use
status_list=[None,None]
times = []
nframe =0 
df = pandas.DataFrame(columns=["start","end"])

while True:
    nframe +=1   #first frame initailization
    check,frame = video.read()  #reading frames of the camera

    #for the time analysis
    status = 0

    #gray scale for acuracy
    gimg = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gimg = cv2.GaussianBlur(gimg,(21,21),0)

     #if cur is the first frame add to baseframe then break
    if nframe == 1:
        bframe=gimg
        continue

    #for difference checking
    deltaframe = cv2.absdiff(bframe,gimg)
    #for the calculation of the contour
    thrframe = cv2.threshold(deltaframe,30,255,cv2.THRESH_BINARY)[1]
    #to smooth the frame 
    thrframe = cv2.dilate(thrframe, None, iterations=2)


    #cal the counter it is nothing but the area of the vectors/block having same color 
    (cnts,_)=cv2.findContours(thrframe.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cont in cnts:
        #to check for change more than 
        if cv2.contourArea(cont) < 2000:
            continue
        status = 1

        #fectch the coordinates of the counter
        (x,y,w,h) = cv2.boundingRect(cont)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3) #making rectangle intheb main frame

    #for analysis adding change in sataus and datetime in times\

    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now()) 


    #showing frames
    cv2.imshow("gray frame",deltaframe)
    cv2.imshow("captunring",gimg)
    cv2.imshow("thrframe",thrframe)
    cv2.imshow("result",frame)
    key=cv2.waitKey(1)

    #to close the frames and recording closing window time in times
    if key == ord("q"):
        times.append(datetime.now())
        times.append(datetime.now())
        break


print(status_list)
print(times)

#updating Dataframes 
for i in range(0,len(times),2):
    df = df.append({"start":times[i],"end":times[i+1]},ignore_index=True)
        
df.to_csv("times.csv")
video.release() 
cv2.destroyAllWindows()