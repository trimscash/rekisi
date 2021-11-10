import cv2
import os
import numpy as np
import sys
import math

args=sys.argv

videoName=f"{args[1]}"
print(videoName)
foldername=args[1].replace(".mp4","")
kore ='/'
dirname=foldername+kore
print(dirname)
os.makedirs(dirname,exist_ok=True)

shotFrame=200
black_dif_threshold=500
white_dif_threshold=200
black_threshold=10
white_threshold=150
diffValue=100

video_data=cv2.VideoCapture(videoName)
if video_data.isOpened() == False:
    print('Video file is not opened.')
    sys.exit()

w= math.floor(video_data.get(cv2.CAP_PROP_FRAME_WIDTH)/4)
h= math.floor(video_data.get(cv2.CAP_PROP_FRAME_HEIGHT)/4)


ret, prev_frame = video_data.read()
prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_black=np.count_nonzero(prev_frame_gray<black_threshold)
prev_white=np.count_nonzero((prev_frame_gray>40)&( prev_frame_gray<70))#めんどいから変数名変えてないけどここはオレンジ色を探してる
stop_counter = 0
i=0
j=0

while True:
    if not(stop_counter%shotFrame):
        video_data.set(cv2.CAP_PROP_POS_FRAMES, stop_counter)
        ret, frame = video_data.read()
        if ret:
            frame = cv2.resize(frame, dsize=(w,h))
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            black = np.count_nonzero(frame_gray < black_threshold)
            white = np.count_nonzero((frame_gray>40)&(frame_gray<70))
            # Picture=frame
            print(black)
            print(white)

            if abs(prev_black-black)>=black_dif_threshold:
                j=0
                cv2.imwrite( f'{dirname}{i}_{j}.png', frame)
                i+=1
            # cv2.imwrite(f'{i}.png', Picture)
            else:
                if abs(prev_white-white)>=white_dif_threshold:
                    # c = video_data.get(cv2.CAP_PROP_POS_FRAMES)
                    j += 1
                    cv2.imwrite(f'{dirname}{i}_{j}.png', frame)
            prev_frame_gray=frame_gray
            prev_black=black
            prev_white=white
        else:
            break
    stop_counter+=1


video_data.release()


for a in range(i):
    picture = []
    b=0
    while True:
        filename=f'{dirname}{a}_{b}.png'
        b+=1
        if os.path.isfile(filename):
            gray=cv2.imread(filename,0)
            picture.append(np.count_nonzero((gray>40)&(gray<70)))
        else:
            break
    print(picture)
    index=picture.index(max(picture))
    print(index)
    for k in range(b-1):
        if k!=index:
            filename = f'{dirname}{a}_{k}.png'
            os.remove(filename)
