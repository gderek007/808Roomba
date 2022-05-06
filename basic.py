import mercury
#From this library https://github.com/gotthardp/python-mercuryapi
from  pycreate2 import Create2
#From this library https://github.com/MomsFriendlyRobotCompany/pycreate2/blob/master/examples/runExample.py
import time
import random as r
#ls on dev and choose cu.usbmodemXXXXXX
reader = mercury.Reader("tmr:///dev/cu.usbmodem142301")
reader.set_region("EU3")
reader.set_read_plan([4], "GEN2")
#print tags 
tags = (reader.read())
for i in tags:
    print(i.rssi, i)

# RFID Tag Names Names
# {300833B2DDD9014000000000 , E28011700000020A7B2E8D44, E200001D5607014724307EB8 , E28011700000020F4CB328F0, 
# E2004740D42BFE4A755E1887, E2000020780A003117906133, E2801170000002118067C4E5, E20043B7034FB3891A4627D1}

tag_dictionary = {}
total_tags_names, identified_tags  = set() , set()
total_tags_names = {'300833B2DDD9014000000000' , 'E28011700000020A7B2E8D44', 'E200001D5607014724307EB8' , 'E28011700000020F4CB328F0', \
'E2004740D42BFE4A755E1887', 'E2000020780A003117906133', 'E2801170000002118067C4E5', 'E20043B7034FB3891A4627D1'}
closest_tag, wanted_tag = 0 , 0

def getClosestTag():
    tags = reader.read()
    tags.sort(key = lambda x: abs(x.rssi) )
    return tags[0] 

def getTagName(tag):
    return str(tag.epc)[2:-1]

while (True):
    #synchronous reading
    #have not tested
    closest_tag = getClosestTag()
    #move robot forward
    if abs( closest_tag.rssi ) < 55 :
        if ( getTagName(closest_tag) == (wanted_tag) ) :
            identified_tags.add( wanted_tag )
            tags_left = total_tags_names - identified_tags
            # gets a random tag from our wanted set
            wanted_tag = r.sample(tags_left, 1) [0]
    else :
        previous_reading = abs(closest_tag.rssi)
        # rotate robot CW
        # do some sort of reading and moving until the rssi goes up
        post_reading = abs(closest_tag.rssi)
        delta = post_reading - previous_reading
        # positive delta means new reading is worst than old reading, therefore rotate CCW
        if delta > 0 :
            #might be last time to rotate right so drive forward somehow
            #rotate left
            #command to rotate for some amount of seconds
            pass
        else :
            #rotate right some more to get more readings
            #rotate right
            #command to rotate for some amount of seconds
            pass

# Create a Create2 Robot
# port = "/dev/tty.usbserial-DN0289CJ"  
# bot = Create2(port)
# bot.start()
# bot.safe()
# bot.full()
# bot.drive_direct(100, 100)
# time.sleep(2)
# bot.drive_direct(200,-200)  # inputs for motors are +/- 500 max
# time.sleep(2)
# bot.drive_stop()

# asynchronous reading set up
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
#time.sleep(1)
#reader.stop_reading()
