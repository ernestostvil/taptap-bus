import time
import gps
#<<<<<<< HEAD
#=======
import time
#>>>>>>> 1d1c28cb71586ef74e0ec804dde61764b7e7216e

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    # time.sleep(3)
    try:
        report = session.next()
#<<<<<<< HEAD
            # Wait for a 'TPV' report and display the current time
            # To see all report data, uncomment the line below
            # print report
        if report['class'] == 'TPV':
            if hasattr(report, 'time'):
                print(report.time)

#=======
        # Wait for a 'TPV' report and display the current time
        # To see all report data, uncomment the line below
        # print report

        if report['class'] == 'TPV':
            if (hasattr(report, 'lat') and hasattr(report, 'lon') and hasattr(report, 'time')):
                print(report.lat)
                print(report.lon)
                print(report.time)

#>>>>>>> 1d1c28cb71586ef74e0ec804dde61764b7e7216e
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
    print("GPSD has terminated")

