import RPi.GPIO as io
import time
import GPS
from gps import *

####from RestAPI import RestAPI====
# from RestAPI import RestAPI


io.setmode(io.BCM)
io.setup(20, io.IN)

man = 0
status = 0
##restAPI = RestAPI()
while 1:
    if io.input(20) == 1:
        man = man + 1
        ##restAPI.postUbicacion(2,3)
        currentHour = time.localtime().tm_hour
        print (" detecto %d" % (man))
        status = 1
        ##print "hora %d" %(currentHour)
        gpsp = GPS.GpsPoller()
        gpsp.start()
        time.sleep(1)
        print ('latitude', gpsp.fix.latitude)
        print ("longitude", gpsp.fix.longitude)
        print ('time', gpsp.fix.time)

        gpsp.stopController()

    # gpsp.start()
    #  print 'latitude',gpsp.current_value.fix.latitude

    elif io.input(20) == 0:
        print("no dectetado")
        status = 0
    time.sleep(3)