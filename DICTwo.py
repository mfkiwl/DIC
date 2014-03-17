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
import time

# Размер шаблона (Квадратный Width * Width)
templateWidth = 10 
# Размер области поиска
matchZoneWidth = 20

img_names = glob.glob("Images/ohtcfrp*.tif")

img1 = cv2.imread(img_names[0], 0)
img2 = cv2.imread(img_names[5], 0)

img1Copy = img1.copy()

h, w = img1.shape[:2]
rows = int(math.floor(h / templateWidth))
cols = int(math.floor(w / templateWidth))

print w, h
print '---'

method = cv2.TM_SQDIFF_NORMED

if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    shouldMinLoc = True
else:
    shouldMinLoc = False

lines = np.zeros((rows * cols, 2), np.int32)

halfTemplateWidth = int(templateWidth / 2)
halfTemplateMatchzoneWidth = int((templateWidth - matchZoneWidth) / 2)
halfMatchZoneWidth = int(matchZoneWidth / 2)

displacementField = np.zeros((rows, cols, 2), np.float32)

prevTime = time.time()

for i in xrange(rows):
    for j in xrange(cols):
        # Индексы текущего шаблона
        templateStartingIndexX = j * templateWidth
        templateStartingIndexY = i * templateWidth
        templateStopIndexX = templateStartingIndexX + templateWidth
        templateStopIndexY = templateStartingIndexY + templateWidth        
        
        # Находим индексы текущей области поиска
        matchZoneStartingIndexX = templateStartingIndexX + halfTemplateMatchzoneWidth
        if matchZoneStartingIndexX < 0:
            matchZoneStartingIndexX = 0
        matchZoneStartingIndexY = templateStartingIndexY + halfTemplateMatchzoneWidth
        if matchZoneStartingIndexY < 0:
            matchZoneStartingIndexY = 0
        matchZoneStopIndexX = matchZoneStartingIndexX + matchZoneWidth
        matchZoneStopIndexY = matchZoneStartingIndexY + matchZoneWidth
        
        #print matchZoneStartingIndexX, matchZoneStartingIndexY
        
        currentTemplate = img2[templateStartingIndexY : templateStopIndexY, templateStartingIndexX : templateStopIndexX]
        currentMatchZone = img1[matchZoneStartingIndexY : matchZoneStopIndexY, matchZoneStartingIndexX : matchZoneStopIndexX]
        
        result = cv2.matchTemplate(currentMatchZone, currentTemplate, method)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        
        if shouldMinLoc:
            neededLoc = minLoc
        else:
            neededLoc = maxLoc 
        
        interpolatedMatchZone = img1[matchZoneStartingIndexX + neededLoc[0] - 1 : matchZoneStartingIndexX + neededLoc[0] + templateWidth, 
                                     matchZoneStartingIndexY + neededLoc[1] - 1 : matchZoneStartingIndexY + neededLoc[1] + templateWidth]    
        
        if interpolatedMatchZone.shape == (11, 11):
            interpolatedMatchZone = cv2.pyrUp(interpolatedMatchZone)
            currentTemplate = cv2.pyrUp(currentTemplate)
            result = cv2.matchTemplate(interpolatedMatchZone, currentTemplate, method)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
            
            print result.shape
            
        relativePosition = (neededLoc[0] - halfTemplateWidth, neededLoc[1] - halfTemplateWidth)
        displacementField.itemset((i, j, 0), relativePosition[0])
        displacementField.itemset((i, j, 1), relativePosition[1])
                             
        lineX = templateStartingIndexX + halfTemplateWidth
        lineY = templateStartingIndexY + halfTemplateWidth
        lineXStop = lineX + relativePosition[0]
        lineYStop = lineY + relativePosition[1]
        cv2.line(img1Copy, (lineX, lineY), (lineXStop, lineYStop), 255, 2) 
        
       # print lineX, lineXStop, lineY, lineYStop
       # relativeMaxLoc = (minLoc[0] - halfMatchZoneWidth, minLoc[1] - halfMatchZoneWidth)
        '''
        lineX = templateStartingIndexX - halfTemplateMatchzoneWidth
        lineY = templateStartingIndexY - halfTemplateMatchzoneWidth
        lineXStop = templateStartingIndexX + neededLoc[0]
        lineYStop = templateStartingIndexY + neededLoc[1]
        cv2.line(img1Copy, (lineX, lineY), (lineXStop, lineYStop), 255, 2)    
        '''
        
        
print time.time() - prevTime

cv2.imshow('res', img1Copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
