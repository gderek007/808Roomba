import mercury
from  pycreate2 import Create2
import time
import random as r
# reader = mercury.Reader("tmr:///dev/cu.usbserial-AQ00WAJ1")
reader = mercury.Reader("tmr:///dev/cu.usbmodem142301")
reader.set_region("EU3")
reader.set_read_plan([4], "GEN2")
tags = (reader.read())
for i in tags:
    print(i.rssi, i)

tag_dictionary = {}
set_tags, identified_tags  = set() , set()
closest_tag, wanted_tag = 0 , 0

while (True):
    tags = reader.read()
    tags.sort(key = lambda x: abs(x.rssi) )
    closest_tag = tags[0] 
    if abs(closest_tag.rssi) < 55 :
        if (closest_tag == wanted_tag) :
            identified_tags.add(wanted_tag)
            tags_left = set_tags - identified_tags
            wanted_tag = r.sample(tags_left, 1) [0]

    





# Create a Create2.
# port = "/dev/tty.usbserial-DN0289CJ"  # where is your serial port?
# bot = Create2(port)

# bot.start()
# bot.safe()
# bot.full()
# bot.drive_direct(100, 100)
# time.sleep(2)
# bot.drive_direct(200,-200)  # inputs for motors are +/- 500 max
# time.sleep(2)
# bot.drive_stop()






# reader.start_reading(lambda tag: print("Name: " + str(tag.epc)[2:-1], "RSSI: " + str(tag.rssi)))

# def nearest_tag(tag):
#     rssi = tag.rssi
#     if 
# def stats_received(stats):
#     print({"temp" : stats.temperature})
#     print({"antenna" : stats.antenna})
#     print({"protocol" : stats.protocol})
#     print({"frequency" : stats.frequency})
#     print(stats)

# reader.enable_stats(stats_received)
time.sleep(1)
reader.stop_reading()