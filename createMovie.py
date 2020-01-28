# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 15:39:16 2020

@author: Azumi Mamiya
"""

import cv2

img = cv2.imread("./TSP_GA_Image/merged_image/0.png")  
height, width, _ = img.shape
image_size = (width, height)  

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video = cv2.VideoWriter('video.mp4', fourcc, 20.0, image_size)


for i in range(1500):
    print(i)
    img = cv2.imread('./TSP_GA_Image/merged_image/{}.png'.format(i))
    img = cv2.resize(img, image_size)
    video.write(img)

video.release()