import os
import cv 
import sys
import gui
import config
import logging
import logging.config
import pygame
import datetime
import qrcode
import server.http 
import stats
import Queue
    
##############################################################################
EVT_PICTURE   = pygame.USEREVENT+1
EVT_COUNTDOWN = pygame.USEREVENT+2
EVT_BTN_BLINK = pygame.USEREVENT+3

##############################################################################
def PrintUsage():
    print """Usage: photobooth.bat <settings_ini>
       where
           <settings_ini> = INI configuration file

       Example: 
           photobooth.bat event1conf\settings.ini
"""

##############################################################################
def CreateQrCode(str, color = "black"):
    qr = qrcode.QRCode( 
            version = 1, 
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            box_size = 6, 
            border = 4 )
    qr.add_data(str)
    qr.make(fit=True)
    pi = qr.make_image()
    
    cv_im = cv.CreateImageHeader(pi.size, cv.IPL_DEPTH_8U, 3)
    cv.SetData(cv_im, pi.tostring())
    return cv_im

##############################################################################
def SetMaintenanceMode(maint_mode):
    global maintenance_mode
    
    maintenance_mode = maint_mode
    if maint_mode:
        # Put photobooth in maintenance mode
        pygame.time.set_timer(EVT_BTN_BLINK, 0)
        gui.init(screen)
        gui.display_brb_screen(screen, "Please wait...", "I need to be serviced")
        pygame.event.clear()
        logger.info("PHOTOBOOTH BRB")
    else:
        # Resume normal photobooth operation
        gui.init(screen)
        gui.display_title_screen(screen, config.TITLE1, config.TITLE2, config.PRESS_BTN_TEXT)
        pygame.time.set_timer(EVT_BTN_BLINK, config.BTN_BLINK_RATE)
        pygame.event.clear()
        logger.info("RESUME OPERATION")

##############################################################################
def StartSession():
    global countdown_timer 
    
    logger.info("START CAPTURE %d" % (stats.incr_session_count()))
    # turn off blink timer
    pygame.time.set_timer(EVT_BTN_BLINK, 0)               
    # start picture taking timer
    pygame.time.set_timer(EVT_PICTURE, int(config.DELAY_SECS * 1000))
    # start countdown update timer
    countdown_timer = config.DELAY_SECS
    pygame.time.set_timer(EVT_COUNTDOWN, 1000)
    # update screen
    gui.bg_redraw(screen)
    gui.show_all_thumbnail_markers(screen)
    gui.show_thumbnail_marker(screen, 0, config.MARKER_SELECT_COLOR)
    gui.display_delay(screen, "Get Ready...", countdown_timer)
    pygame.display.flip()

##############################################################################
def StopSession(screen, capturedImages, event_dir):
    pygame.time.set_timer(EVT_PICTURE, 0)
    pygame.time.set_timer(EVT_COUNTDOWN, 0)
    
    # Compose final image
    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
    (finalImg, dest_file) = ProcessImages(capturedImages, event_dir, filename)
    
    # Send photobooth picture to printer
    if config.PRINT_COPIES > 0:
        numCopies = min(config.PRINT_COPIES, 3) # just in case 
        for i in range(numCopies):
            logger.info("PRINTING %d of %d..." % (i+1, numCopies))
            config.PRINT_FUNC(config.PRINTER_NAME, dest_file)

    # Display final image
    pygame.time.wait(800)
    DisplayFinalPicture(screen, finalImg)
    pygame.time.wait(config.FINAL_IMG_SHOW_DELAY);

    # Reset event timers and GUI for next session
    gui.display_title_screen(screen, config.TITLE1, config.TITLE2, config.PRESS_BTN_TEXT)
    pygame.time.set_timer(EVT_BTN_BLINK, config.BTN_BLINK_RATE)
    pygame.event.clear()
    logger.info("EVENTS CLEARED")

##############################################################################
def ProcessImages(imgs, dest_dir, filename):
    dest_file = "%s\\%s" % (dest_dir, filename)
    qrImg = None

    # Create QR code if configured
    if config.QR_CODE:
        qrcode_url = "%s/%s/%s" % (config.QR_BASE_URL, config.EVENT_NAME, filename[:-4])
        qrImg = CreateQrCode(qrcode_url, config.QR_CODE_COLOR)
        logger.info("QR code: %s" % (qrcode_url))

    # Create photobooth picture from captured images and QR code
    finalPic = config.LAYOUT_FUNC(imgs, config.FINAL_IMG_LOGO_FILE, qrImg)

    # Save final photobooth picture                
    logger.info("Saving image to %s" % (dest_file))
    cv.SaveImage(dest_file, finalPic)
    stats.add_image_roll(filename)

    return (finalPic, dest_file)
    
##############################################################################
def DisplayFinalPicture(screen, finalPic):
    gui.bg_redraw(screen)

    # Show photobooth picture on gui
    showImg = cv.CreateImage((int(finalPic.width*config.FINAL_IMG_DISPLAY_SIZE), int(finalPic. height*config.FINAL_IMG_DISPLAY_SIZE)), finalPic.depth, finalPic.nChannels)
    cv.Resize(finalPic, showImg)
    cv.CvtColor(showImg, showImg, cv.CV_BGR2RGB)

    pg_img = pygame.image.frombuffer( showImg.tostring(), cv.GetSize(showImg), "RGB" )

    screen.blit( pg_img, (int((screen.get_width() - pg_img.get_width())/2), config.FINAL_IMG_DISPLAY_POS_TOP))
    gui.display_done_text(screen, "All Done!", "Your pictures are being printed")
    pygame.display.flip()

##############################################################################
winpos_x = 200
winpos_y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (winpos_x,winpos_y)

# Read config settings
if len(sys.argv) != 2:
    PrintUsage()
    sys.exit(1)   

settings_file = sys.argv[1]
if not os.path.exists(settings_file):
    print "Settings file does not exist: %s" % (settings_file)
    sys.exit(2)
config.read_settings(settings_file)

# Setup logging module
logging.config.fileConfig(config.LOGGING_CONF)
logger = logging.getLogger("main")
logger.info("PROGRAM START")

# Check base directory and event directory exists
if not os.path.exists(config.PHOTO_DIRECTORY):
    logger.error("Base directory does not exist: %s" % (config.PHOTO_DIRECTORY))
    sys.exit(3)
event_dir = "%s\\%s" % (config.PHOTO_DIRECTORY, config.EVENT_NAME)
if not os.path.exists(event_dir):
    os.makedirs(event_dir)

# Get camera handle
camera  = cv.CaptureFromCAM(0)
cv.SetCaptureProperty(camera, cv.CV_CAP_PROP_FRAME_WIDTH, config.CAM_CAPTURE_WIDTH)
cv.SetCaptureProperty(camera, cv.CV_CAP_PROP_FRAME_HEIGHT, config.CAM_CAPTURE_HEIGHT)

# Get test frame to check if webcam is working
frame = cv.QueryFrame(camera)
if frame is None:
    logger.critical("Can't get frame.  No webcam attached?")
    del(camera)
    sys.exit(4)
   
# Pygame initialization   
pygame.init()
if config.FULLSCREEN:
    pygame.mouse.set_visible(False)
flags = pygame.FULLSCREEN if config.FULLSCREEN else 0
window = pygame.display.set_mode( (config.WINDOW_SIZE_WIDTH, config.WINDOW_SIZE_HEIGHT), flags)
pygame.display.set_caption( "Photobooth" )
screen = pygame.display.get_surface()

# Initialize GUI
gui.init(screen)

# Initialize stats module
stats.clear_all()

# Start HTTP server
cmdQ = Queue.Queue()
http_server = server.http.HttpServer(event_dir, stats, cmdQ)
http_server.start()

# Display title screen and start press button text blink timer
gui.display_title_screen(screen, config.TITLE1, config.TITLE2, config.PRESS_BTN_TEXT)
pygame.time.set_timer(EVT_BTN_BLINK, config.BTN_BLINK_RATE)

# Initialize variables
capturedImages = []
filterFn = None
on_exit = False
maintenance_mode = False
capture_in_progress = False
countdown_timer = 0

# Main processing loop
while not on_exit :    
    events = pygame.event.get()

    for event in events:
        if event.type == EVT_COUNTDOWN:
            #######################################################
            # Decrement time displayed until next picture is taken
            #######################################################
            logger.info("EVT_COUNTDOWN")
            countdown_timer = countdown_timer - 1
            gui.display_delay(screen, "Get Ready...", countdown_timer)
            if countdown_timer <= 1:
                pygame.time.set_timer(EVT_COUNTDOWN, 0)                
        elif event.type == pygame.KEYDOWN:
            #######################################################
            # Handle keystrokes
            #######################################################
            logger.info("EVT_KEYDOWN: " + str(event))
            
            if (event.key == pygame.K_ESCAPE or event.key == pygame.K_q):
                # Quit
                on_exit = True 
            elif not capture_in_progress:
                if (event.key == pygame.K_m):
                    # Toggle maintenance mode
                    SetMaintenanceMode(not maintenance_mode)
                elif not maintenance_mode:
                    if (event.key == pygame.K_x):
                        # Clear filter
                        filterFn = None
                        logger.info("Clear filterFn")
                    #elif (event.key == pygame.K_BACKSLASH):
                        # (Had a stuck key on keyboard)
                        # ignore, do nothing
                        #logger.info("Ignoring key", event.key)
                    elif (event.key in config.layouts.keys()):
                        # Change GUI and print layout
                        logger.info("Switch to layout %s" % config.layouts[event.key])
                        config.read_layout_ini(config.layouts[event.key]['ini'])
                        config.FINAL_IMG_LOGO_FILE = config.layouts[event.key]['logo_file']
                        gui.init(screen)
                        gui.display_title_screen(screen, config.TITLE1, config.TITLE2, config.PRESS_BTN_TEXT)
                    elif (event.key in config.filters.keys()):
                        # Apply filter
                        logger.info("Apply filter %s" % event.key)
                        filterFn = config.filters[event.key]
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_p or config.ANY_KEY_STARTS:   
                        # Start picture taking session
                        capture_in_progress = True
                        capturedImages = []
                        StartSession()
        elif event.type == EVT_PICTURE:
            #######################################################
            # Take a picture (save and process frame)
            #######################################################
            logger.info("EVT_PICTURE %d" % (len(capturedImages)+1))
            saveImg = cv.CreateImage((cropFrame.width, cropFrame.height), cropFrame.depth, cropFrame.nChannels)
            cv.Resize(cropFrame, saveImg)
            capturedImages.append(saveImg)
            gui.show_thumbnail(screen, cropFrame, len(capturedImages)-1)
            
            if (len(capturedImages) >= config.NUM_IMAGES):
                # Done taking pictures, stop current session                
                capture_in_progress = False
                StopSession(screen, capturedImages, event_dir)
            else:
                # Reset event timers and GUI for next picture in current session
                pygame.time.set_timer(EVT_COUNTDOWN, 0)
                countdown_timer = config.DELAY_SECS
                pygame.time.set_timer(EVT_COUNTDOWN, 1000)
                gui.show_thumbnail_marker(screen, len(capturedImages), config.MARKER_SELECT_COLOR)
                gui.display_delay(screen, "Get Ready...", countdown_timer)
        elif event.type == EVT_BTN_BLINK:
            ####################################################
            # Blink press button text
            ####################################################
            gui.blink_btn_text(screen)
        elif event.type == pygame.QUIT:
            ####################################################
            # Quit program
            ####################################################
            logger.info("EVT_QUIT" + str(event))
            on_exit = True

    # Process command queue
    if not capture_in_progress:
        try:
            cmd = cmdQ.get(False).strip()
            logger.info("Rcvd HTTP_CMD [%s]" % (cmd))
            
            if cmd[0:4] == "VKEY" and not maintenance_mode:
                # Virtual keypress
                key = cmd[5]
                keydata = { 'key': ord(key.lower()),
                            'unicode': key          }
                vkey_event = pygame.event.Event(pygame.KEYDOWN, keydata)
                pygame.event.post(vkey_event)
            elif cmd == "BRB":
                # Put photobooth in maintenance mode
                SetMaintenanceMode(True)
            elif cmd == "RESUME":
                # Resume normal photobooth operation
                SetMaintenanceMode(False)
            else:
                # Unknown command
                logger.warn("Unknown HTTP_CMD [%s]" % (cmd))
        except Queue.Empty:
            pass

    # Capture/process frame
    if not (on_exit or maintenance_mode):        
        # Grab a frame
        frame = cv.QueryFrame(camera)

        # Crop according to config settings
        cropFrame = gui.crop_image(frame, (0, 0, min(frame.width, int(frame.width/config.CAM_ASPECT_RATIO)), min(frame.height, int(frame.width * config.CAM_ASPECT_RATIO))))

        # Apply filter to captured frame
        if filterFn is not None:
            filterImg = filterFn(cropFrame) 
            cropFrame = filterImg  

        # Update frame
        gui.show_frame(screen, cropFrame, config.CAM_FRAME_SIZE, config.CAM_BORDER_WIDTH, config.CAM_BORDER_COLOR)
        
    # Delay per FPS setting
    pygame.time.delay( int( 1000.0 / config.FPS ) )

# Clean up
del(camera)
pygame.display.quit()
pygame.quit()
http_server.stop()
logger.info("PROGRAM END")
