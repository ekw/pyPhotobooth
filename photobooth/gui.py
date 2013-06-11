import pygame
import config
import cv
import os

bg_image = None
header_img = None

##############################################################################
def init(screen):
    global bg_image
    global header_img
    
    bg_image = pygame.Surface(screen.get_size())
    fill_gradient(bg_image, config.BG_COLOR, config.GRADIENT_COLOR)
    
    # Load GUI header image if specified
    if os.path.exists(config.HEADER_IMG_FILE):
        header_img = cv.LoadImage(config.HEADER_IMG_FILE, cv.CV_LOAD_IMAGE_COLOR)
    else:
        header_img = None

##############################################################################
def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    """fill a surface with a gradient pattern
    Parameters:
    color -> starting color
    gradient -> final color
    rect -> area to fill; default is surface's rect
    vertical -> True=vertical; False=horizontal
    forward -> True=forward; False=reverse
    
    Pygame recipe: http://www.pygame.org/wiki/GradientCode
    """
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    if vertical: h = y2-y1
    else:        h = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    rate = (
        float(b[0]-a[0])/h,
        float(b[1]-a[1])/h,
        float(b[2]-a[2])/h
    )
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1,y2):
            color = (
                min(max(a[0]+(rate[0]*(line-y1)),0),255),
                min(max(a[1]+(rate[1]*(line-y1)),0),255),
                min(max(a[2]+(rate[2]*(line-y1)),0),255)
            )
            fn_line(surface, color, (x1,line), (x2,line))
    else:
        for col in range(x1,x2):
            color = (
                min(max(a[0]+(rate[0]*(col-x1)),0),255),
                min(max(a[1]+(rate[1]*(col-x1)),0),255),
                min(max(a[2]+(rate[2]*(col-x1)),0),255)
            )
            fn_line(surface, color, (col,y1), (col,y2))
            
##############################################################################
def display_centered_text(screen, vPos, renderedStr):
    strRect = renderedStr.get_rect()
    strRect.y, strRect.centerx = vPos, screen.get_rect().width / 2
    screen.blit(renderedStr, strRect)

##############################################################################
def bg_redraw(screen):
    screen.blit(bg_image, (0,0))

##############################################################################
def bg_redraw_rect(screen, rect):
    rect = rect.inflate(5,5)
    screen.set_clip(rect)
    screen.blit(bg_image, (0,0))
    screen.set_clip(None)
    
##############################################################################
blink_rect = None
blink_text = None
blink_mod = 0
def display_title_screen(screen, line1, line2, press_button_text):
    global blink_rect
    global blink_text    
    
    bg_redraw(screen)
    
    lrg_font = pygame.font.SysFont(config.TITLE_FONT, config.LARGE_FONT_SIZE)
    font = pygame.font.SysFont(config.TITLE_FONT, config.MEDIUM_FONT_SIZE)
    
    pos_Y = config.HEADER_POS_Y
    
    if header_img is not None:
        display_size = (int(header_img.width), int(header_img.height))
        matImg = cv.CreateImage(display_size, header_img.depth, header_img.nChannels)
        cv.Resize(header_img, matImg)
        cv.CvtColor(matImg, matImg, cv.CV_BGR2RGB)
        
        pg_header_img = pygame.image.frombuffer( matImg.tostring(), cv.GetSize(matImg), "RGB" )
        imgRect = pg_header_img.get_rect()
        imgRect.y, imgRect.centerx = pos_Y, screen.get_rect().width / 2
        screen.blit( pg_header_img, imgRect)
    else:
        line1Text = lrg_font.render(line1, 1, config.TITLE_COLOR)
        display_centered_text(screen, pos_Y, line1Text)
    
        line2Text = lrg_font.render(line2, 1, config.TITLE_COLOR)
        display_centered_text(screen, pos_Y + 90, line2Text)
    
    line3Text = font.render(press_button_text, 1, config.TITLE_COLOR)
    blink_rect = line3Text.get_rect()
    blink_rect.y, blink_rect.centerx = screen.get_rect().height * config.PRESS_BTN_TEXT_POS, screen.get_rect().width / 2
    blink_text = line3Text
    display_centered_text(screen, screen.get_rect().height * config.PRESS_BTN_TEXT_POS, line3Text)
    
    show_all_thumbnail_markers(screen)
    
    pygame.display.flip()

##############################################################################
def display_brb_screen(screen, line1, line2):
    bg_redraw(screen)
    
    lrg_font = pygame.font.SysFont(config.TITLE_FONT, config.LARGE_FONT_SIZE)
    pos_Y = screen.get_rect().height * 0.35
    
    line1Text = lrg_font.render(line1, 1, config.TITLE_COLOR)
    display_centered_text(screen, pos_Y, line1Text)

    line2Text = lrg_font.render(line2, 1, config.TITLE_COLOR)
    display_centered_text(screen, pos_Y + 90, line2Text)
    
    pygame.display.flip()

##############################################################################
def blink_btn_text(screen):
    global blink_mod
    
    blink_mod = blink_mod + 1
    if (blink_mod % 2):
        screen.set_clip(blink_rect.inflate(3,3))
        screen.blit(bg_image, (0,0))
        screen.set_clip(None)
    else:
        display_centered_text(screen, screen.get_rect().height * config.PRESS_BTN_TEXT_POS, blink_text)
    pygame.display.flip()
    
    
##############################################################################
def display_done_text(screen, line1, line2):    
    lrg_font = pygame.font.SysFont(config.TITLE_FONT, config.LARGE_FONT_SIZE)
    font = pygame.font.SysFont(config.TITLE_FONT, config.MEDIUM_FONT_SIZE)
    
    pos_Y = screen.get_rect().height * 0
    
    line1Text = lrg_font.render(line1, 1, config.TITLE_COLOR)
    display_centered_text(screen, pos_Y, line1Text)
    
    line2Text = font.render(line2, 1, config.TITLE_COLOR)
    display_centered_text(screen, pos_Y + 100, line2Text)
       
##############################################################################
def display_delay(screen, line_text, secs_left):
    font = pygame.font.SysFont(config.STATUS_FONT, config.MEDIUM_FONT_SIZE)
    
    readyText = font.render(line_text, 1, config.STATUS_COLOR)
    readyRect = readyText.get_rect()
    readyRect.y, readyRect.centerx = config.COUNTDOWN_Y_POS, screen.get_rect().width / 2
    bg_redraw_rect(screen, readyRect)
    screen.blit(readyText, readyRect)

    countText = font.render( "%d" % secs_left, 1, config.STATUS_COLOR)
    countRect = countText.get_rect()
    countRect.y, countRect.centerx = config.COUNTDOWN_Y_POS + countRect.height, screen.get_rect().width / 2
    bg_redraw_rect(screen, countRect)
    screen.blit(countText, countRect)
    
    pygame.display.update(readyRect)
    pygame.display.update(countRect)
        
##############################################################################
def show_thumbnail(screen, img, i):
    th_width = int(img.width * config.THUMBNAIL_SIZE)
    th_height = int(img.height * config.THUMBNAIL_SIZE)
    
    thumbImg = cv.CreateImage((th_width, th_height), img.depth, img.nChannels)
    cv.Resize(img, thumbImg)                
    cv.CvtColor(thumbImg, thumbImg, cv.CV_BGR2RGB)
            
    pg_img0 = pygame.image.frombuffer( thumbImg.tostring(), cv.GetSize(thumbImg), "RGB" )  

    rect = (int(screen.get_rect().width * config.THUMBNAIL_X_POS), config.THUMBNAIL_Y_POS + (i * (th_height + 20)))
    screen.blit(pg_img0, rect)
    pygame.draw.rect(screen, config.THUMBNAIL_COLOR, ((rect),(pg_img0.get_width(), pg_img0.get_height())), 2)
    pygame.display.flip()

##############################################################################
def show_all_thumbnail_markers(screen):
    for i in range(config.NUM_IMAGES):
        show_thumbnail_marker(screen, i, config.MARKER_COLOR)
        
##############################################################################
def show_thumbnail_marker(screen, i, color):
    th_width = int(min(config.CAM_CAPTURE_WIDTH, config.CAM_CAPTURE_WIDTH/config.CAM_ASPECT_RATIO) * config.THUMBNAIL_SIZE)
    th_height = int( min(config.CAM_CAPTURE_HEIGHT, config.CAM_CAPTURE_WIDTH * config.CAM_ASPECT_RATIO) * config.THUMBNAIL_SIZE)
    
    topleft = (int(screen.get_rect().width * config.THUMBNAIL_X_POS), int(config.THUMBNAIL_Y_POS + (i * (th_height + 20))))
    marker = pygame.Rect(topleft, (th_width, th_height))
    marker = marker.inflate(-3,-3)
    pygame.draw.rect(screen, color, marker, 2)
    
    font = pygame.font.SysFont(config.THUMBNAIL_FONT, config.LARGE_FONT_SIZE)
    
    numText = font.render("%d" % (i+1), 1, color)
    numRect = numText.get_rect()
    numRect.centery, numRect.centerx = marker.centery, marker.centerx
    screen.blit(numText, numRect)
      
##############################################################################
def crop_image(img, region):
    cv.SetImageROI(img, region)
    cropImg = cv.CreateImage((region[2], region[3]), img.depth, img.nChannels)    
    cv.Copy(img, cropImg)
    return cropImg

##############################################################################
def show_frame(screen, takeImg, shrink, border_width, border_color):
    display_size = (int(takeImg.width * shrink), int(takeImg.height * shrink))
    matImg = cv.CreateImage(display_size, takeImg.depth, takeImg.nChannels)
    cv.Resize(takeImg, matImg)
    cv.CvtColor(matImg, matImg, cv.CV_BGR2RGB)
    
    pg_img = pygame.image.frombuffer( matImg.tostring(), cv.GetSize(matImg), "RGB" )
    border = pg_img.get_rect().inflate(2*border_width,2*border_width)
    border.centery, border.centerx = \
        (config.CAM_FRAME_POS_TOP+(border.height/2)-(border_width), config.CAM_FRAME_POS_LEFT+(border.width/2)-(border_width))
    pygame.draw.rect(screen, border_color, border)
    screen.blit( pg_img, (config.CAM_FRAME_POS_LEFT, config.CAM_FRAME_POS_TOP))
    pygame.display.flip()
