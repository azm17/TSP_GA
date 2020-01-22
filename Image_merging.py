# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 01:55:41 2020

@author: Azumi Mamiya
"""
import cv2
import numpy as np


for i in range(100):
    image_name = f'{i}.png'
    im1 = cv2.imread('fig_fitness/'+image_name)
    im2 = cv2.imread('graph_best/'+image_name)
    im3 = cv2.imread('graph/'+image_name)
    
    
    im_h = cv2.hconcat([im1, im2, im3])
    cv2.imwrite('merged_image/'+image_name, im_h)