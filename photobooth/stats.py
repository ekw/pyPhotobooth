from datetime import datetime

# Session start time
start_time = datetime.now()
def get_session_start():
    return str(start_time)

# Session count
session_count = 0
def clear_session_count():
    global session_count
    session_count = 0    
def get_session_count():
    return session_count
def incr_session_count():
    global session_count
    session_count = session_count + 1
    return session_count

# running image roll    
image_roll = []
def clear_image_roll():
    global image_roll
    image_roll = []
def add_image_roll(img_path):
    global image_roll
    image_roll.append(img_path)
def get_image_roll():
    return image_roll
def get_lastX_image_roll(x):
    return image_roll[-x]
    
def clear_all():
    clear_session_count()
    clear_image_roll()
    start_time = datetime.now()
    