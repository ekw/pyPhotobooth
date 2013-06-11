import cv

CAL_IMGS = []

def process(img):
    global CAL_IMGS
    
    if len(CAL_IMGS) < 5:
        CAL_IMGS.append(cv.CloneMat(cv.GetMat(img)))
        if len(CAL_IMGS) == 5:
           # last time here, do averaging here
           pass
        return img
    
    # using last of CAL_IMGS, but should use average
    referenceImg = CAL_IMGS[4]
    
    # diffMat contains difference in pixel values between 
    # referenceImg and current frame passed in img
    diffMat = cv.CloneMat(cv.GetMat(img))
    cv.AbsDiff(img, referenceImg, diffMat)
    
    # diffMat contains 255 if difference is greater than thresholdValue
    # 0 otherwise
    thresholdValue = 100
    cv.Threshold(diffMat, diffMat, thresholdValue, 255, cv.CV_THRESH_BINARY)
    
    # Smoothing
    cv.Smooth(diffMat, diffMat, cv.CV_MEDIAN, 15)
    
    # Convert diffMat to grayscale
    gray = cv.CreateImage(cv.GetSize(diffMat), 8, 1)
    cv.CvtColor(diffMat, gray, cv.CV_BGR2GRAY)
    
    # Create final results matrix
    result = cv.CloneMat(cv.GetMat(img))    
    cv.SetZero(result)
    
    # result(I) = src1(I) & src2(I) if mask(I) != 0
    cv.And(img, img, result, gray)
    
    return cv.GetImage(result)
    