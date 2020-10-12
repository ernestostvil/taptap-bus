import threading

import gps
import RPi.GPIO as io
import time
##from RestAPI import RestAPI

io.setmode(io.BCM)
io.setup(20, io.IN)

man = 0
status = 0

def espera():
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    while (True):
        try:
            report = session.next()

            a = 0
            while (a <= 20):
                try:
                    report = session.next()
            #>>>>>>> 52fe1173962b9d4308a2bc65d81fc50d09ba95ea
            # Wait for a 'TPV' report and display the current time
            # To see all report data, uncomment the line below
            # print report
                    if report['class'] == 'TPV':
                        if hasattr(report, 'lat'):
                            print(report.lat)
                except KeyError:
                    pass
                except KeyboardInterrupt:
                    quit()
        except StopIteration:
            session = None
            print("GPSD has terminated")
        time.sleep(5)
        print("Primer Hilo.")


def segundoHilo():
    b = 0
    while b <= 20:
        if io.input(20) == 1:
            man = man + 1
            print(" detecto %d" % (man))
            status = 1
        elif io.input(20) == 0:
            print("no dectetado")
            status = 0
        time.sleep(3)
        print("Segundo Hilo")
        b += 1


subproceso = threading.Thread(name='espera', target=espera)
subproceso.start()

Hilo2 = threading.Thread(name='segundoHilo', target=segundoHilo)
# Hilo2.start()