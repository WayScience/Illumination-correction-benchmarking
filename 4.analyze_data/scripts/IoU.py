#!/usr/bin/env python
# coding: utf-8

# ## Perform Intersection over Union (IoU) analysis on object masks 

# In[1]:


# iou function from stackoverflow user gil.fernandes
# https://stackoverflow.com/questions/66595055/fastest-way-of-computing-binary-mask-iou-with-numpy

import torch
import cv2


# In[2]:


# Intersection over Union function (IoU) utilizing ground truth (gt) and test binary masks 
def iou(gt: torch.Tensor, test: torch.Tensor):
    '''
    Takes in the ground truth (gt) and test images as binary masks. 
    Returns the Intersection over Union (IoU) value. 
    An IoU close to 1 reflects high overlap between the ground truth and test binary masks. 
    An IoU close to 0 refelcts little overlap between the ground truth and test binary masks
    '''
    
    intersection = (gt * test).sum()
    if intersection == 0:
        return 0.0
    union = torch.logical_or(gt, test).to(torch.int).sum()
    return intersection / union 

# Read binary masks 
mask1 = cv2.imread('/home/maggiekeating/M1_B1_01_1_2_DAPI_001_nuclei_mask.tiff', 0)
mask2 = cv2.imread('/home/maggiekeating/M2_B1_01_1_2_DAPI_001_nuclei_mask.tiff', 0)

# Convert binary masks from numpy ndarray to pytorch tensor 
mask1_conv = torch.from_numpy(mask1)
mask2_conv = torch.from_numpy(mask2)

print(iou(mask1_conv, mask2_conv))

