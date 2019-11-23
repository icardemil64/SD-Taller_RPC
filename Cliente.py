import cv2
import numpy as np
import xmlrpc.client
def dibujaMenu(ancho,alto):
    #cv2.line(frame,(0,0),(ancho,alto),(0,255,0),4)
    #cv2.line(frame,(ancho,0),(0,alto),(0,255,0),4)    
    puntoCentral = (ancho//2,alto//2)
    cv2.line(frame,(ancho//2,0),(ancho//2,alto),(0,255,0),4)
    cv2.line(frame,(0,alto//2),(ancho,alto//2),(0,255,0),4)
    cv2.circle(frame,(puntoCentral),7,(0,255,0),-1)
    cv2.putText(frame,'Avanza',(10,50),font,1.75,(0,255,0),3,cv2.LINE_AA)
    cv2.putText(frame,'Retrocede',(ancho - 300,50),font,1.75,(0,255,0),3,cv2.LINE_AA)
    cv2.putText(frame,'Izquierda',(10, alto - 20),font,1.75,(0,255,0),3,cv2.LINE_AA)
    cv2.putText(frame,'Derecha',(ancho - 250, alto - 20),font,1.75,(0,255,0),3,cv2.LINE_AA)

def imprimeCoordenadas(x,y):
    if((x>0 and x<ancho//2) and (y > 0 and y <alto//2)):
        print(conec.avanza())
    elif(x>ancho//2 and x < ancho and (y > 0 and y <alto//2)):
        print(conec.retrocede())
    elif((x>0 and x<ancho//2) and (y > alto//2 and y <alto)):
        print(conec.izquierda())
    else:
        print(conec.derecha())

cap = cv2.VideoCapture(0)
ancho = int(cap.get(3))
alto = int(cap.get(4))

conec = xmlrpc.client.ServerProxy("http://192.168.43.148:8000/")

tiempo = 40
print((ancho,alto))

rojoBajo = np.array([100,100,20],np.uint8)
rojoAlto = np.array([125,255,255],np.uint8)

rojoBajo2 = np.array([175,100,20],np.uint8)
rojoAlto2 = np.array([179,255,255],np.uint8)

count = tiempo
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)
    dibujaMenu(ancho,alto)
    if ret == True:
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #maskRojo1 = cv2.inRange(frameHSV,rojoBajo,rojoAlto)
        #maskRojo2 = cv2.inRange(frameHSV,rojoBajo2,rojoAlto2)
        mask = cv2.inRange(frameHSV,rojoBajo,rojoAlto)
        #mask = cv2.add(maskRojo1,maskRojo2)
        contornos,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in contornos:
            area = cv2.contourArea(c)
            #if area > 7000:
            if area > 3000:
                M = cv2.moments(c)
                if (M["m00"]==0):
                    M["m00"] = 1
                x = int(M["m10"]/M["m00"])
                y = int(M["m01"]/M["m00"])
                count=count-1
                if count == 0:
                    imprimeCoordenadas(x,y)
                    count = tiempo
                cv2.circle(frame,(x,y),7,(0,0,255),-1)
                cv2.putText(frame,'{},{}'.format(x,y),(x+10,y),font,0.75,(0,255,0),1,cv2.LINE_AA)
                contornoFino = cv2.convexHull(c)
                cv2.drawContours(frame,[contornoFino],0,(255,0,0),3)
        cv2.imshow('Segundo taller de Sistemas Distribuidos, 2019',frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

cap.release()
cv2.destroyAllWindows()