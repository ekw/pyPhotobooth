import threading
import random
import cherrypy
import os
from cherrypy.lib.static import serve_file

# HttpServer used to get latest picture taken, get a random picture 
# or command photobooth to perform some command (show halt message 
# while changing ink, etc.)

class HttpRoot(object):

    def __init__(self, photo_dir, booth_stats, cmdQ):
        self.photo_dir = photo_dir
        self.booth_stats = booth_stats
        self.cmdQ = cmdQ
        self.abs_photo_dir = "%s\\%s" % (os.path.join(os.path.abspath(os.curdir)), photo_dir)

        self.last_latestrand = None
        self.last_rand = None
        
    @cherrypy.expose
    def index(self):
        return "Welcome to Photobooth!"

    # Serve the given image file
    @cherrypy.expose
    def picture(self, name):
        return serve_file("%s\\%s" % (self.abs_photo_dir, name))

    # Return latest image(s)
    @cherrypy.expose
    def latest(self, num=1):
        n = max(1, int(num))
        images = self.booth_stats.get_image_roll()
        totalNum = len(images)
        if totalNum == 0:
            return "No pictures taken yet"
        elif n==1:
            return serve_file("%s\\%s" % (self.abs_photo_dir, images[-1]))
        else:
            httpstr = ""
            get = min(totalNum, n)
            pics = images[-get:]
            pics.reverse()
            for pic in pics:
                httpstr += "%s<BR><img width='750' src='http://localhost:8080/picture/%s'><BR><HR>" % (pic, pic)
            return httpstr

    # Return random image
    @cherrypy.expose
    def rand(self):
        images = self.booth_stats.get_image_roll()

        if len(images) > 1:
            randChoice = random.choice(images)
            while randChoice == self.last_rand:
                randChoice = random.choice(images)                
            self.last_rand = randChoice
            return serve_file("%s\\%s" % (self.abs_photo_dir, randChoice))
        elif len(images) == 1:
            return self.latest(1)
        else:
            return "No pictures taken yet"

    # If there's a new image, return latest image or else return a random image
    @cherrypy.expose
    def latestrand(self):
        images = self.booth_stats.get_image_roll();
        latestImg = images[-1]
        if self.last_latestrand == latestImg:
            return self.rand();
        else:
            self.last_latestrand = latestImg
            return serve_file("%s\\%s" % (self.abs_photo_dir, latestImg))

    # Return photobooth stats
    @cherrypy.expose
    def stats(self):
        httpstr = "Session start: %s<BR>Pictures taken: %d" % (self.booth_stats.get_session_start(), self.booth_stats.get_session_count())
        return httpstr

    # Put photobooth in maintenance mode
    @cherrypy.expose
    def brb(self):
        self.cmdQ.put("BRB")
        return "BRB cmd sent"

    # Resume normal photobooth operations
    @cherrypy.expose
    def resume(self):
        self.cmdQ.put("RESUME")
        return "RESUME cmd sent"

    # Send virtual keypress to photobooth
    @cherrypy.expose
    def vkey(self, key=None):
        if key is not None:
            cmd = "VKEY:%s" % key[0]
            self.cmdQ.put(cmd)
            return "%s cmd sent" % (cmd)
        else:
            return "No key given"

class HttpServer(threading.Thread):
    
    def __init__(self, photo_dir, booth_stats, cmdQ):
        self.photo_dir = photo_dir
        self.booth_stats = booth_stats
        self.cmdQ = cmdQ
        random.seed()
        threading.Thread.__init__(self)
        
    def run(self):
        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.quickstart(HttpRoot(self.photo_dir, self.booth_stats, self.cmdQ))
        
    def stop(self):
        cherrypy.engine.exit()