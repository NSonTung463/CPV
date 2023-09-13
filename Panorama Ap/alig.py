import cv2
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import glob
    
def stand_img(img):
    img = cv2.resize(img,(600,400))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img 
def delete_files_in_folder(folder_path):
    # Kiểm tra xem thư mục tồn tại hay không
    if not os.path.exists(folder_path):
        return

    # Lặp qua tất cả các file trong thư mục
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Kiểm tra xem đối tượng có phải là file hay không
        if os.path.isfile(file_path):
            # Xóa file
            os.remove(file_path)
def stitch_img(images):
    # Khởi tạo đối tượng Stitcher
    stitcher = cv2.Stitcher_create()
    status, stitched_image = stitcher.stitch(images)
    if status == cv2.Stitcher_OK:
        # Nếu thành công, trả về ảnh đã ghép
        stitched_image = stand_img(stitched_image)
        return stitched_image
    else:
        # Nếu không thành công, in ra thông báo lỗi
        print("Không thể ghép ảnh.")
        return None

# Gọi hàm để xóa toàn bộ file trong thư mục
def get_frame_video(path):
    delete_files_in_folder('./stitch_images')
    cap = cv2.VideoCapture(path)
    frame,ret = cap.read()
    cntFrame=0
    while 1:
        ret,frame = cap.read()

        if ret:
            cv2.imwrite("./stitch_images/img{:04d}.jpg".format(cntFrame), frame)
            print('img ',cntFrame)
            cv2.waitKey(10)
            cntFrame+=1
            k = cv2.waitKey(20)
        else: break
    cap.release()
    return cntFrame
def get_frame():
    delete_files_in_folder('./captured_images')
    delete_files_in_folder('./dis_img')
    cntFrame = 0 
    for filename in os.listdir('./stitch_images'):
        file_path = os.path.join('./stitch_images', filename)
        # Kiểm tra xem đối tượng có phải là file hay không
        if os.path.isfile(file_path):
            cntFrame += 1
    idxs = np.linspace(0,cntFrame,50).astype('int')
    imgs = []
    
    for idx in idxs:
        img = cv2.imread("stitch_images/img{:04d}.jpg".format(idx))
        cv2.imwrite("./captured_images/img{:04d}.jpg".format(idx), img)

def function_1():
    image_paths = glob.glob("captured_images/*.jpg")
    images = []
    for image_path in image_paths:
        image = cv2.imread(image_path)
        if image is not None:
            images.append(image)
    stitch_img(images)
    return stitch_img(images)
def function_2():
    delete_files_in_folder('./captured_images')
def function_3():
    return None
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def stitching(image_paths):
    imgs = []
    for i in range(len(image_paths)):
        img = cv.imread(image_paths[i])
        img = cv.resize(img, (224, 224))
        imgs.append(img)
  
    stitchy=cv.Stitcher.create()
    (dummy,output)=stitchy.stitch(imgs)

    return output


def stitching_build(path0, path1):

    src_img = cv.imread(path0)
    tar_img = cv.imread(path1)
    
    src_gray = cv.cvtColor(src_img, cv.COLOR_RGB2GRAY)
    tar_gray = cv.cvtColor(tar_img, cv.COLOR_RGB2GRAY)

    SIFT_detector = cv.SIFT_create()
    kp1, des1 = SIFT_detector.detectAndCompute(src_gray, None)
    kp2, des2 = SIFT_detector.detectAndCompute(tar_gray, None)

    bf = cv.BFMatcher(cv.NORM_L2, crossCheck=False)

    rawMatches = bf.knnMatch(des1, des2, 2)
    matches = []
    ratio = 0.75

    for m,n in rawMatches:
        if m.distance < n.distance * 0.75:
            matches.append(m)

    matches = sorted(matches, key=lambda x: x.distance, reverse=True)
    matches = matches[:200]

    img3 = cv.drawMatches(src_img, kp1, tar_img, kp2, matches, None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    kp1 = np.float32([kp.pt for kp in kp1])
    kp2 = np.float32([kp.pt for kp in kp2])

    pts1 = np.float32([kp1[m.queryIdx] for m in matches])
    pts2 = np.float32([kp2[m.trainIdx] for m in matches])

    (H, status) = cv.findHomography(pts1, pts2, cv.RANSAC)

    h1, w1 = src_img.shape[:2]
    h2, w2 = tar_img.shape[:2]
    result = cv.warpPerspective(src_img, H, (w1+w2, h1))
    result[0:h2, 0:w2] = tar_img
    
    return result

#
# imgs = stitching_build("img/img0.jpg", "img/img1.jpg")
# plt.imshow(imgs)
# plt.show()

