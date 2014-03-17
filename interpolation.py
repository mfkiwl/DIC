# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 21:50:02 2014

@author: Cyrill Nadezhdin, KSTU - KAI, 2014
"""

import cv2
import numpy as np
import time

src = cv2.imread('logo.jpg', 0)
# dst = np.zeros((512, 512, 1), np.uint8)
# rows, cols, depth = dst.shape
time1 = time.time()
print 34 % 15
print time.time() - time1
cv2.imshow('image', src)
cv2.waitKey(0)
cv2.destroyAllWindows()
