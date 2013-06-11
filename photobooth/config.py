import ConfigParser

WINDOW_SIZE_WIDTH = 1280
WINDOW_SIZE_HEIGHT = 960 
FULLSCREEN = False
DELAY_SECS = 0.8
COUNTDOWN_Y_POS = 50
FPS = 24.0
PHOTO_DIRECTORY = "..\\events"
EVENT_NAME = "test"
QR_CODE = False
QR_BASE_URL = "http://www.lawong.com"
QR_CODE_COLOR = (0,0,0)
ANY_KEY_STARTS = True
FILTER_CONFIG = "filters.ini"
CAM_CAPTURE_WIDTH = 960.0
CAM_CAPTURE_HEIGHT = 720.0
CAM_FRAME_POS_LEFT = 70
CAM_FRAME_POS_TOP = 240
CAM_FRAME_SIZE = 0.9 # percent of CAM_CAPTURE_WIDTH/CAM_CAPTURE_HEIGHT
CAM_BORDER_COLOR = (0,0,0)
CAM_BORDER_WIDTH = 5
CAM_ASPECT_RATIO = 0.59

THUMBNAIL_X_POS = 0.77 # percent of screen width
THUMBNAIL_Y_POS = CAM_FRAME_POS_TOP - CAM_BORDER_WIDTH # absolute
THUMBNAIL_SIZE = 0.25 # percent of capture frame width/height

PRINT_COPIES = 0
PRINTER_NAME = "Canon MG5300 series Printer"
PRINT_PKG = "print"
PRINT_MODULE = "winPrint"
PRINT_FUNCNAME = "print_image"
PRINT_FUNC = None

NUM_IMAGES = 4
FINAL_IMG_DISPLAY_SIZE = 0.33
FINAL_IMG_DISPLAY_POS_TOP = 200
FINAL_IMG_SHOW_DELAY = 7 * 1000 # ms
FINAL_IMG_LAYOUT_PKG = "layouts"
FINAL_IMG_LAYOUT_MODULE = "layout"
FINAL_IMG_LAYOUT_FUNC = "Four4by6"
FINAL_IMG_LOGO_FILE = "sampleLogo1.jpg"
LAYOUT_FUNC = None

HEADER_POS_Y = 10 # absolute
PRESS_BTN_TEXT_POS = 0.80 # percent of screen height
BTN_BLINK_RATE = 500 # ms

BG_COLOR = (5, 242, 251)        # Top
GRADIENT_COLOR = (0, 120, 255)  # Bottom
MARKER_COLOR = (50,50,50)
MARKER_SELECT_COLOR = (255,255,255)

LARGE_FONT_SIZE = 60
MEDIUM_FONT_SIZE = 45

TITLE_FONT = 'Verdana'
TITLE_COLOR = (255, 0, 0)

STATUS_FONT = 'Verdana'
STATUS_COLOR = (255, 0, 0)

THUMBNAIL_FONT = 'Verdana'
THUMBNAIL_COLOR = MARKER_COLOR

HEADER_IMG_FILE = "header.jpg"
TITLE1 = "Title1" 
TITLE2 = "Title2"
PRESS_BTN_TEXT = "press button text"

filters = {}
layouts = {}

def read_settings(file):
    global EVENT_NAME, HEADER_IMG_FILE, TITLE1, TITLE2, PRESS_BTN_TEXT 
    global HEADER_POS_Y, BTN_BLINK_RATE 
    global BG_COLOR, GRADIENT_COLOR, MARKER_COLOR, MARKER_SELECT_COLOR 
    global CAM_BORDER_COLOR
    global LARGE_FONT_SIZE, MEDIUM_FONT_SIZE 
    global TITLE_FONT, TITLE_COLOR 
    global STATUS_FONT, STATUS_COLOR 
    global THUMBNAIL_FONT, THUMBNAIL_COLOR 
    global WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT, FULLSCREEN
    global QR_CODE, ANY_KEY_STARTS, FINAL_IMG_LOGO_FILE
    global DELAY_SECS, COUNTDOWN_Y_POS, FPS 
    global PHOTO_DIRECTORY, QR_BASE_URL, QR_CODE_COLOR 
    global PRINT_COPIES, PRINTER_NAME, PRINT_PKG, PRINT_MODULE, PRINT_FUNCNAME, PRINT_FUNC
    global LOGGING_CONF, FILTER_CONFIG
    global filters, layouts
    
    config = ConfigParser.SafeConfigParser()
    config.read(file)
    
    EVENT_NAME      = config.get("Event", "EVENT_NAME")
    HEADER_IMG_FILE = config.get("Event", "HEADER_IMG_FILE")
    TITLE1          = config.get("Event","TITLE1")
    TITLE2          = config.get("Event","TITLE2")
    PRESS_BTN_TEXT  = config.get("Event","PRESS_BTN_TEXT")
    
    HEADER_POS_Y        = config.getint("GUI", "HEADER_POS_Y")
    BTN_BLINK_RATE      = config.getint("GUI", "BTN_BLINK_RATE")
    BG_COLOR            = eval(config.get("GUI", "BG_COLOR"))
    GRADIENT_COLOR      = eval(config.get("GUI", "GRADIENT_COLOR"))
    MARKER_COLOR        = eval(config.get("GUI", "MARKER_COLOR"))
    MARKER_SELECT_COLOR = eval(config.get("GUI", "MARKER_SELECT_COLOR"))
    CAM_BORDER_COLOR    = eval(config.get("GUI", "CAM_BORDER_COLOR"))
    LARGE_FONT_SIZE     = config.getint("GUI", "LARGE_FONT_SIZE")
    MEDIUM_FONT_SIZE    = config.getint("GUI", "MEDIUM_FONT_SIZE")
    TITLE_FONT          = config.get("GUI", "TITLE_FONT")
    TITLE_COLOR         = eval(config.get("GUI", "TITLE_COLOR"))
    STATUS_FONT         = config.get("GUI", "STATUS_FONT")
    STATUS_COLOR        = eval(config.get("GUI", "STATUS_COLOR"))
    THUMBNAIL_FONT      = config.get("GUI", "THUMBNAIL_FONT")
    THUMBNAIL_COLOR     = eval(config.get("GUI", "THUMBNAIL_COLOR"))
	 
    WINDOW_SIZE_WIDTH   = config.getint("System", "WINDOW_SIZE_WIDTH")
    WINDOW_SIZE_HEIGHT  = config.getint("System", "WINDOW_SIZE_HEIGHT")
    FULLSCREEN          = config.getboolean("System", "FULLSCREEN")
    QR_CODE             = config.getboolean("System", "QR_CODE")
    ANY_KEY_STARTS      = config.getboolean("System", "ANY_KEY_STARTS")
    DELAY_SECS          = config.getfloat("System", "DELAY_SECS")
    COUNTDOWN_Y_POS     = config.getint("System", "COUNTDOWN_Y_POS")
    FPS                 = config.getfloat("System", "FPS")
    PHOTO_DIRECTORY      = config.get("System", "PHOTO_DIRECTORY")
    LOGGING_CONF        = config.get("System", "LOGGING_CONF")
    QR_BASE_URL         = config.get("System", "QR_BASE_URL")
    QR_CODE_COLOR       = eval(config.get("System", "QR_CODE_COLOR"))
    FILTER_CONFIG       = config.get("System", "FILTER_CONFIG")
    FINAL_IMG_SHOW_DELAY= config.getint("System", "FINAL_IMG_SHOW_DELAY")

    PRINT_COPIES        = config.getint("Print", "PRINT_COPIES")
    PRINTER_NAME        = config.get("Print", "PRINTER_NAME")
    PRINT_PKG           = config.get("Print", "PRINT_PKG")
    PRINT_MODULE        = config.get("Print", "PRINT_MODULE")
    PRINT_FUNCNAME      = config.get("Print", "PRINT_FUNCNAME")
    
    # Retrieve print function
    print_pkg = __import__("%s.%s" % (PRINT_PKG, PRINT_MODULE))
    print_module = getattr(print_pkg, PRINT_MODULE)
    PRINT_FUNC = getattr(print_module, PRINT_FUNCNAME)
    
    # Read layout config and save keys
    for layoutnum in range(0,10):
        layout_section = "Layout%d" % (layoutnum)
        if config.has_section(layout_section):
            layout_key = config.get(layout_section, "LAYOUT_KEY")
            layout_ini = config.get(layout_section, "LAYOUT_INI")
            layout_logo = config.get(layout_section, "LAYOUT_LOGO")
            layouts[ord(layout_key)] = { 'ini': layout_ini, 'logo_file': layout_logo }
            if (layoutnum == 0):
                read_layout_ini(layout_ini)
                FINAL_IMG_LOGO_FILE = layout_logo
    
    # Read filter config and save keys
    filterconfig = ConfigParser.SafeConfigParser()
    filterconfig.read(FILTER_CONFIG)
    for filternum in range(0,30):
        filter_section = "Filter%d" % (filternum)
        if filterconfig.has_section(filter_section):
           filter_key =  filterconfig.get(filter_section, "FILTER_KEY")           
           mod_name = "%s.%s" % (filterconfig.get(filter_section, "FILTER_PKG"), filterconfig.get(filter_section, "FILTER_MODULE")) 
           filter_pkg = __import__(mod_name)
           filter_module = getattr(filter_pkg, filterconfig.get(filter_section, "FILTER_MODULE"))
           filter_func = getattr(filter_module, filterconfig.get(filter_section, "FILTER_FUNC"))
           filters[ord(filter_key)] = filter_func

def read_layout_ini(file):
    global CAM_CAPTURE_WIDTH, CAM_CAPTURE_HEIGHT 
    global CAM_FRAME_POS_LEFT, CAM_FRAME_POS_TOP, CAM_FRAME_SIZE 
    global CAM_BORDER_WIDTH, CAM_ASPECT_RATIO 
    global THUMBNAIL_X_POS, THUMBNAIL_Y_POS, THUMBNAIL_SIZE 
    global PRESS_BTN_TEXT_POS
    global FINAL_IMG_DISPLAY_POS_TOP, FINAL_IMG_SHOW_DELAY 
    global FINAL_IMG_LAYOUT_PKG, FINAL_IMG_LAYOUT_MODULE, FINAL_IMG_LAYOUT_FUNC 
    global NUM_IMAGES, FINAL_IMG_DISPLAY_SIZE
    global LAYOUT_FUNC
    
    config = ConfigParser.SafeConfigParser()
    config.read(file)
    
    CAM_CAPTURE_WIDTH   = config.getfloat("CamFrame", "CAM_CAPTURE_WIDTH")
    CAM_CAPTURE_HEIGHT  = config.getfloat("CamFrame", "CAM_CAPTURE_HEIGHT")
    CAM_FRAME_POS_LEFT  = config.getint("CamFrame", "CAM_FRAME_POS_LEFT")
    CAM_FRAME_POS_TOP   = config.getint("CamFrame", "CAM_FRAME_POS_TOP")
    CAM_FRAME_SIZE      = config.getfloat("CamFrame", "CAM_FRAME_SIZE")
    CAM_ASPECT_RATIO    = config.getfloat("CamFrame", "CAM_ASPECT_RATIO")
    CAM_BORDER_WIDTH    = config.getint("CamFrame", "CAM_BORDER_WIDTH")

    THUMBNAIL_X_POS     = config.getfloat("CamFrame", "THUMBNAIL_X_POS")
    THUMBNAIL_Y_POS     = eval(config.get("CamFrame", "THUMBNAIL_Y_POS"))
    THUMBNAIL_SIZE      = config.getfloat("CamFrame", "THUMBNAIL_SIZE")
    PRESS_BTN_TEXT_POS  = config.getfloat("CamFrame", "PRESS_BTN_TEXT_POS")

    FINAL_IMG_DISPLAY_POS_TOP = config.getint("FinalImage", "FINAL_IMG_DISPLAY_POS_TOP")
    FINAL_IMG_LAYOUT_PKG      = config.get("FinalImage", "FINAL_IMG_LAYOUT_PKG")
    FINAL_IMG_LAYOUT_MODULE   = config.get("FinalImage", "FINAL_IMG_LAYOUT_MODULE")
    FINAL_IMG_LAYOUT_FUNC     = config.get("FinalImage", "FINAL_IMG_LAYOUT_FUNC")
    
    # Read image layout parameters
    pkgName = "%s.%s" % (FINAL_IMG_LAYOUT_PKG, FINAL_IMG_LAYOUT_MODULE)
    layoutPkg = __import__(pkgName)
    layoutModule = getattr(layoutPkg, FINAL_IMG_LAYOUT_MODULE)
    LAYOUT_FUNC = getattr(layoutModule, FINAL_IMG_LAYOUT_FUNC)
    NUM_IMAGES = getattr(layoutModule, "NUM_IMAGES")
    FINAL_IMG_DISPLAY_SIZE = getattr(layoutModule, "FINAL_IMG_DISPLAY_SIZE")
