import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
cam=cv2.VideoCapture(0)
face_detector=FaceMeshDetector(maxFaces=1)


counter=0

memes={"closing eyes": cv2.imread(r"C:\Users\Tast\Desktop\IT\Ai Projects\Computer_Vision\reaction\memes\closing eye.jpg"),
           "kissing": cv2.imread(r"C:\Users\Tast\Desktop\IT\Ai Projects\Computer_Vision\reaction\memes\kissing.jpg"),
           "sarcastic": cv2.imread(r"C:\Users\Tast\Desktop\IT\Ai Projects\Computer_Vision\reaction\memes\sarcastic.jpg"),
           "silly smile": cv2.imread(r"C:\Users\Tast\Desktop\IT\Ai Projects\Computer_Vision\reaction\memes\silly_smile.jpg"), 
           "shocked": cv2.imread(r"C:\Users\Tast\Desktop\IT\Ai Projects\Computer_Vision\reaction\memes\shocked.JPG"),
        }


CONFIRM_FRAMES = 5
RESET_FRAMES = 12
up_counter = 0
down_counter = 0
candidate = None
shown = None

while True:
    ok,frame=cam.read()
    frame=cv2.flip(frame,1)
    frame, face_list = face_detector.findFaceMesh(frame, draw=True)
    reaction=None
    


    
    if face_list:
        
        face = face_list[0]

        upperlip=face[13][1]
        lowerlip=face[14][1]

        head_up=face[10][1]
        head_down=face[152][1]

        right_down_eye=face[145][1]
        right_up_eye=face[159][1] 

        left_down_eye=face[374][1]
        left_up_eye=face[386][1]

        lip_left=face[61][0]
        lip_right=face[291][0]

        head_left=face[234][0]
        head_right=face[454][0]

        lip_angle_left=face[61][1]
        lip_angle_right=face[291][1]



        
        corners_y_avg=(lip_angle_left+lip_angle_right)/2

        distance_lip_width=abs(lip_right-lip_left)

        distance_lip_up_down=abs(upperlip-lowerlip)

        distance_head_hieght=abs(head_up-head_down)

        distance_head_width=abs(head_right-head_left)

        right_eye_height=abs(right_up_eye-right_down_eye)

        left_eye_height=abs(left_up_eye-left_down_eye)

        open_mouth=abs(distance_lip_up_down/distance_head_hieght)

        mouth_smile=abs(distance_lip_width/distance_head_width)

        right_eye_open=abs(right_eye_height/distance_head_hieght)
        left_eye_open=abs(left_eye_height/distance_head_hieght)
        corner_lift=(upperlip-corners_y_avg)/distance_head_hieght

        open_eye=(right_eye_open+left_eye_open)/2
        print("head_left",head_left)

        print("head_right",head_right)
        print("head_up",head_up)
        print("head_down",head_down)
        print("------------------------------------")

       

        if open_mouth>0.04 and corner_lift>- 0.006:
            reaction="silly smile" 
        elif open_mouth>= 0.04 and open_eye>= 0.07:
            reaction="shocked" 
        elif  mouth_smile< 0.3:
            reaction="kissing"
        elif open_eye<0.018:
            reaction="closing eyes"
        elif corner_lift>0.02:
            reaction="sarcastic"

    if reaction is not None:
         down_counter = 0
         if reaction == candidate:

          up_counter += 1
         else:
          candidate = reaction
          up_counter = 1

         if up_counter >= CONFIRM_FRAMES:
           shown = reaction
    else:
        candidate = None
        up_counter = 0
        down_counter += 1
        if down_counter >= RESET_FRAMES:
         shown = None

    if shown is not None and face_list:
     size = 200
     half = size // 2
     h, w = frame.shape[:2]
     meme_image = cv2.resize(memes[shown], (size, size))
     cy = (head_up + head_down) // 2
     cx = (head_left + head_right) // 2
     if cx - half >= 0 and cy - half >= 0 and cx + half <= w and cy + half <= h:
             frame[cy-half:cy+half, cx-half:cx+half] = meme_image
         

    
    cv2.imshow("reaction cam",frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows() 