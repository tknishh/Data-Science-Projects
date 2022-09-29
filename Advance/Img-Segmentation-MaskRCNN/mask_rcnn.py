import cv2
import numpy as np

net = cv2.dnn.readNetFromTensorflow("dnn/frozen_inference_graph_coco.pb",
                                    "dnn/mask_rcnn_inception_v2_coco_2018_01_28.pvtxt")

classesFile = "coco.names"
classNames = open(classesFile).read().strip().split('\n')

img = cv2.imread("img.jpg")
height, width, _ =  img.shape

blank_mask = np.zeros((height,width,3), np.uint8)
blank_mask[:]= (0,0,0)

blob = cv2.dnn.blobFromImage(img, swapRB=True)

net.setInput(blob)

boxes, masks = net.forward(['detection_out_final',"detection_masks"])
detection_count = boxes.shape[2]

count = 0
for i in range(detection_count):
    box = boxes[0,0,i]
    class_id = int(box[1])
    score = box[2]
    if score > 0.6:
        continue
    class_name = (classNames[class_id])
    x = int(box[3]* width)
    y = int(box[4]* height)
    x2 = int(box[5]* width)
    y2 = int(box[6]* height)

    roi = blank_mask[y:y2, x:x2]
    roi_height, roi_width, _ = roi.shape

    mask = masks[i, int(class_id)]
    mask = cv2.resize(mask, (roi_widht, roi_height))
    _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)
    coutn+=1

    contours, _ = cv2.findContours(np.array(mask. np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    color = np.random.randint(0, 255, 3, dtype='uint8')
    color =[int(c) for c in color]

    for cnt in contours:
        cv2.fillPoly(roi, [cnt], (int(color[0], int(color[1]), int(color[2]))))


    cv2.rectangle(img, (x,y), (x2,y2), color, 2)
    cv2.putText(img, class_name, (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

alpha = 1 
beta = 0.8
mask_img = cv2.addWeighted(img, alpha, blank_mask, beta, 0)

cv2.imshow("Black image", blank_mask)
cv2.imshow("Mask Image", img)
cv2.waitKey(0)