# -*- coding: utf-8 -*-
"""
Created on Thu Mar 06 12:24:43 2014

@author: Cyrill Nadezhdin, KSTU - KAI, 2014
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob
import math

# Размер шаблона (Квадратный Width * Width)
templateWidth = 10 
# Размер области поиска
matchZoneWidth = 30

img_names = glob.glob("Images/ohtcfrp*.tif")

img1 = cv2.imread(img_names[0], 0)
img2 = cv2.imread(img_names[5], 0)

img1Copy = img1.copy()

h, w = img1.shape[:2]
rows = int(math.floor(h / matchZoneWidth))
cols = int(math.floor(w / matchZoneWidth))

print w, h
print '---'

method = cv2.TM_SQDIFF_NORMED

lines = np.zeros((rows * cols, 2), np.int32)

for i in xrange(rows):
    for j in xrange(cols):
        # Находим индексы текущей области поиска
        matchZoneStartingIndexX = j * matchZoneWidth
        matchZoneStartingIndexY = i * matchZoneWidth
        matchZoneStopIndexX = matchZoneStartingIndexX + matchZoneWidth
        matchZoneStopIndexY = matchZoneStartingIndexY + matchZoneWidth
        
        # Индексы текущего шаблона
        templateStartingIndexX = matchZoneStartingIndexX + int(matchZoneWidth / 2)
        templateStartingIndexY = matchZoneStartingIndexY + int(matchZoneWidth / 2)
        templateStopIndexX = templateStartingIndexX + templateWidth
        templateStopIndexY = templateStartingIndexY + templateWidth
        
        #print matchZoneStartingIndexX, matchZoneStartingIndexY
        
        currentTemplate = img2[templateStartingIndexY : templateStopIndexY, templateStartingIndexX : templateStopIndexX]
        currentMatchZone = img1[matchZoneStartingIndexY : matchZoneStopIndexY, matchZoneStartingIndexX : matchZoneStopIndexX]
        
        result = cv2.matchTemplate(currentMatchZone, currentTemplate, method)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        

        relativeMaxLoc = (minLoc[0] - int(matchZoneWidth / 2), minLoc[1] - int(matchZoneWidth / 2))
        lineX = templateStartingIndexX + relativeMaxLoc[0]
        lineY = templateStartingIndexY + relativeMaxLoc[1]
        cv2.line(img1Copy, (lineX, lineY), (templateStartingIndexX, templateStartingIndexY), 255, 2)
        
        

cv2.imshow('res', img1Copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
