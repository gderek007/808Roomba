from ast import Pass
import mercury
#From this library https://github.com/gotthardp/python-mercuryapi
from  pycreate2 import Create2
#From this library https://github.com/MomsFriendlyRobotCompany/pycreate2
import time
import random as r
#ls on dev and choose cu.usbmodemXXXXXX
reader = mercury.Reader("tmr:///dev/cu.usbmodem14301")
reader.set_region("EU3")
reader.set_read_plan([4], "GEN2")

# RFID Tag Names Names
# {300833B2DDD9014000000000 , E28011700000020A7B2E8D44, E200001D5607014724307EB8 , E28011700000020F4CB328F0, 
# E2004740D42BFE4A755E1887, E2000020780A003117906133, E2801170000002118067C4E5, E20043B7034FB3891A4627D1}

#dict might be useful to map name to RSSI? not too sure tho 
tag_dictionary = {}
total_tags_names, identified_tags  = set() , set()
# ordered ABC from our sticky notes, A-H
total_tags_names = {'E2004740D42BFE4A755E1887' , 'E28011700000020F4CB328F0', 'E200001D5607014724307EBD', '300833B2DDD9014000000000', \
    'E2801170000002118067C4E5', 'E20043B7034FB3891A4627D1', 'E2000020780A003117906133', 'E28011700000020A7B2E8D44'}
closest_tag, wanted_tag = 0 , 'E2004740D42BFE4A755E1887'

def getClosestTag():
    tags = reader.read()
    tags.sort(key = lambda x: abs(x.rssi) )
    # for i in tags:
    #     print( getTagName(i) , i.rssi  )
    # print()
    return tags[0] 

def getTagName(tag):
    return str(tag.epc)[2:-1]

while (True):
    #synchronous reading
    #have not tested
    closest_tag = getClosestTag()
    #(print( getTagName(closest_tag) , closest_tag.rssi  ))
    #move robot forward
    if (len(identified_tags) == len(total_tags_names)) :
        break
    if abs( closest_tag.rssi ) <= 60 :
        # TODO might have to change this approach to just grab any tag not specifically the wanted tag
        # just check if the tag has been discovered already
        if ( getTagName(closest_tag) not in identified_tags ) :
            print("Found: ", getTagName(closest_tag), closest_tag.rssi)
            identified_tags.add( getTagName(closest_tag) )
            tags_left = total_tags_names - identified_tags
            print("Tags Left:", len(tags_left))
            # gets a random tag from our wanted set
            wanted_tag = r.sample(tags_left, 1) [0]
            # clean for some amount of time
            # TODO code for cleaning around the RFID Tag
    else :
        previous_reading = abs(closest_tag.rssi)
        # TODO rotate robot CW
        # TODO do some sort of reading and moving until the rssi goes up
        old_tag = closest_tag
        closest_tag = getClosestTag()
        # TODO not sure how yet but veryify that we arent going after a tag we have seen already, cause would waste time
        if (closest_tag == old_tag) :
            pass
        else:
            # tag changed? make sure dont move
            time.sleep(1)
            closest_tag = getClosestTag()
        post_reading = abs(closest_tag.rssi)
        delta = post_reading - previous_reading
        # positive delta means new reading is worst than old reading, therefore rotate CCW
        if delta > 0 :
            #might be last time to rotate right so drive forward somehow
            # TODO rotate left
            # TODO command to rotate for some amount of seconds
            pass
        else :
            #rotate right some more to get more readings
            #TODO rotate right
            #TODO command to rotate for some amount of seconds
            pass


print("Done")
# TODO set up for the Creat2 Robot
# Create a Create2 Robot
# ls on dev and choose usbserial-XXXXXXXX
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

# TODO potential alternative to async read on the fly (might be more difficult)
# asynchronous reading set up
# reader.start_reading(lambda tag: print("Name: " + str(tag.epc)[2:-1], "RSSI: " + str(tag.rssi)))

# v random code not helpful i belive 
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
