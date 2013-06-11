import cv 
from numpy import *

def blackwhite(img):
    filterImg = cv.CreateImage((img.width, img.height), img.depth, 1)
    cv.CvtColor( img, filterImg, cv.CV_RGB2GRAY )
    cv.CvtColor( filterImg, img, cv.CV_GRAY2RGB )
    return img

def erode(img):
    cv.Erode(img, img, iterations=2)
    return img
    
def inverse(img):    
    cv.Not(img, img)
    return img
    
def blackWhiteInverse(img):
    img = blackwhite(img)
    img = inverse(img)
    return img
    
def sepia(img):
    kern = cv.CreateMat(3, 3, cv.CV_32FC1)
    kern = array([ 
           (0.131, 0.534, 0.272),
           (0.168, 0.686, 0.349),
           (0.189, 0.769, 0.393),
           ])
    cv.Transform(img, img, cv.fromarray(kern))
    return img
    