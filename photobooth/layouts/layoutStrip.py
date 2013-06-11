import cv
import os

NUM_IMAGES = 3
FINAL_IMG_WIDTH = 2000
FINAL_IMG_HEIGHT = 3000

FINAL_IMG_QR_CODE_X = 760
FINAL_IMG_QR_CODE_Y = 2560
FINAL_IMG_DIVIDER_WIDTH = 120     # even number
FINAL_IMG_DISPLAY_SIZE = 0.25

FINAL_IMG_BORDER_WIDTH_TOP = 95
FINAL_IMG_BORDER_WIDTH_BOTTOM = 118
FINAL_IMG_BORDER_WIDTH_LEFT = 91 
FINAL_IMG_BORDER_WIDTH_RIGHT = 0

##############################################################################
def ThreeStrip(images, logoFile, qrImg):
    
    p1 = images[0]
    p2 = images[1]
    p3 = images[2]
    
    border_top = FINAL_IMG_BORDER_WIDTH_TOP
    border_bottom = FINAL_IMG_BORDER_WIDTH_BOTTOM
    border_left = FINAL_IMG_BORDER_WIDTH_LEFT
    border_right = FINAL_IMG_BORDER_WIDTH_RIGHT
    divider_width = FINAL_IMG_DIVIDER_WIDTH
    width = FINAL_IMG_WIDTH
    height = FINAL_IMG_HEIGHT
    
    pic_widths = p2.width
    pic_heights = p2.height
    #print "orig w %d h %d" % (pic_widths, pic_heights)
    
    finalImg = cv.CreateImage((width, height), 8, 3)
    cv.Set(finalImg, cv.CV_RGB(255,255,255))
    
    resized_W = int((width - (border_left+border_right) - (divider_width)) / 2)
    resized_H = int((float(resized_W)/pic_widths) * pic_heights)

    # rect = (left, top, width, height)
    # top pics
    rect = (border_left, border_top, resized_W, resized_H)
    cv.SetImageROI(finalImg, rect)
    cv.Resize(p1, finalImg)
    cv.ResetImageROI(finalImg)
    
    rect = (int(border_left + resized_W + (divider_width/2)), border_top, resized_W, resized_H)
    cv.SetImageROI(finalImg, rect)
    cv.Resize(p1, finalImg)
    cv.ResetImageROI(finalImg)
    
    # middle pics
    rect = (border_left, border_top + resized_H + 5, resized_W, resized_H)
    cv.SetImageROI(finalImg, rect)
    cv.Resize(p2, finalImg)
    cv.ResetImageROI(finalImg)
    
    rect = (int(border_left + resized_W + (divider_width/2)), border_top + resized_H + 5, resized_W, resized_H)
    cv.SetImageROI(finalImg, rect)
    cv.Resize(p2, finalImg)
    cv.ResetImageROI(finalImg)
    
    # bottom pics
    rect = (border_left, border_top + (2*(resized_H + 5)), resized_W, resized_H)
    cv.SetImageROI(finalImg, rect)
    cv.Resize(p3, finalImg)
    cv.ResetImageROI(finalImg)
    
    rect = (int(border_left + resized_W + (divider_width/2)), border_top + (2*(resized_H + 5)), resized_W, resized_H)
    cv.SetImageROI(finalImg, rect)
    cv.Resize(p3, finalImg)
    cv.ResetImageROI(finalImg)
    
    logoImg = None
    if os.path.exists(logoFile):
        logoImg = cv.LoadImage(logoFile, cv.CV_LOAD_IMAGE_COLOR)
        
    if (logoImg is not None):
        rect = (border_left, 3*(resized_H+5) + border_top, logoImg.width, logoImg.height)
        cv.SetImageROI(finalImg, rect)
        cv.Resize(logoImg, finalImg)
        cv.ResetImageROI(finalImg)
        
        rect = (int(border_left + resized_W + (divider_width/2)), 3*(resized_H+5) + border_top, logoImg.width, logoImg.height)
        cv.SetImageROI(finalImg, rect)
        cv.Resize(logoImg, finalImg)
        cv.ResetImageROI(finalImg)
        
    if (qrImg is not None):
        rect = (FINAL_IMG_QR_CODE_X, FINAL_IMG_QR_CODE_Y, qrImg.width, qrImg.height)
        cv.SetImageROI(finalImg, rect)
        cv.Resize(qrImg, finalImg)
        cv.ResetImageROI(finalImg)
        
        rect = (FINAL_IMG_QR_CODE_X+945, FINAL_IMG_QR_CODE_Y, qrImg.width, qrImg.height)
        cv.SetImageROI(finalImg, rect)
        cv.Resize(qrImg, finalImg)
        cv.ResetImageROI(finalImg)
        
    return finalImg
