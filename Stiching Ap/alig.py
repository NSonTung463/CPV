import cv2
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import cv2
import os
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np

def stand_img(img):
    img = cv2.resize(img,(600,400))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img 
def feature_align(imgTest,imgRef,orb):
    orb_detector = cv2.ORB_create(orb)
    # Extract key points and descriptors for both images
    keyPoint1, des1 = orb_detector.detectAndCompute(imgTest, None)
    keyPoint2, des2 = orb_detector.detectAndCompute(imgRef, None)
    return keyPoint1, des1,keyPoint2, des2
def drawKeypoints(img1,img2,orb):
    img1 , img2 = stand_img(img1) , stand_img(img2)
    keyPoint1, _,keyPoint2, _ = feature_align(img1,img2,orb)
    im1_display = cv2.drawKeypoints(img1,keyPoint1,outImage= np.array([]), color = (255,0,0), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    im2_display = cv2.drawKeypoints(img2,keyPoint2,outImage= np.array([]), color = (255,0,0), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return im1_display , im2_display
def drawMatch(img1,img2,orb,pc_value):
    img1 = cv2.resize(img1,(600,400))
    img2 = cv2.resize(img2,(600,400))
    keyPoint1, des1,keyPoint2, des2= feature_align(img1,img2,orb)
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(des1, des2, None)
    matches = list(matches)
    matches.sort(key=lambda x: x.distance, reverse=False)
    # Remove not so good matches
    numGoodMatches = int(len(matches) * pc_value)
    matches = matches[:numGoodMatches]
    # Draw top matches
    im_matches = cv2.drawMatches(img1, keyPoint1, img2, keyPoint2, matches, None)
    im_matches = stand_img(im_matches)
    return im_matches
def convert_img(img1,img2,orb,pc_value):
    img1 = cv2.resize(img1,(600,400))
    img2 = cv2.resize(img2,(600,400))
    keyPoint1, des1,keyPoint2, des2 = feature_align(img1,img2,orb)
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(des1, des2, None)
    matches = list(matches)
    matches.sort(key=lambda x: x.distance, reverse=False)
    # Remove not so good matches
    numGoodMatches = int(len(matches) *pc_value)
    matches = matches[:numGoodMatches]
    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)
    for i, match in enumerate(matches):
        points1[i, :] = keyPoint1[match.queryIdx].pt
        points2[i, :] = keyPoint2[match.trainIdx].pt
    # Find homography
    h, mask = cv2.findHomography(points2, points1, cv2.RANSAC)
    #Use homography to warp image
    height, width, channels = img1.shape
    im2_reg = cv2.warpPerspective(img2,h,(width, height))
    img1 , im2_reg = stand_img(img1),stand_img(im2_reg)
    return img1 , im2_reg

