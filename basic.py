from ast import Pass
from logging.handlers import RotatingFileHandler
import mercury
#From this library https://github.com/gotthardp/python-mercuryapi
from  pycreate2 import Create2
#From this library https://github.com/MomsFriendlyRobotCompany/pycreate2
import time
import random as r
#ls on dev and choose cu.usbmodemXXXXXX
reader = mercury.Reader("tmr:///dev/cu.usbmodem14201")
reader.set_region("EU3")
reader.set_read_plan([4], "GEN2")

# RFID Tag Names Names
# {300833B2DDD9014000000000 , E28011700000020A7B2E8D44, E200001D5607014724307EB8 , E28011700000020F4CB328F0, 
# E2004740D42BFE4A755E1887, E2000020780A003117906133, E2801170000002118067C4E5, E20043B7034FB3891A4627D1}

#dict might be useful to map name to RSSI? not too sure tho 
tag_dictionary = {'E2004740D42BFE4A755E1887': 'A', 'E28011700000020F4CB328F0':'B', 'E200001D5607014724307EBD':'C', '300833B2DDD9014000000000':'D', \
    'E2801170000002118067C4E5':'E', 'E20043B7034FB3891A4627D1':'F', 'E2000020780A003117906133':'G', 'E28011700000020A7B2E8D44':'H'}
total_tags_names, identified_tags  = set() , set()
# ordered ABC from our sticky notes, A-H
total_tags_names = {'E2004740D42BFE4A755E1887' , 'E28011700000020F4CB328F0', 'E200001D5607014724307EBD', '300833B2DDD9014000000000', \
    'E2801170000002118067C4E5', 'E20043B7034FB3891A4627D1', 'E2000020780A003117906133', 'E28011700000020A7B2E8D44'}
closest_tag, wanted_tag = 0 , 'E2004740D42BFE4A755E1887'
## ROBOT SETUP:
## set port to usb serial value 
port = '/dev/tty.usbserial-DN0289CJ'  # this is the serial port on my iMac
baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
    }
bot = Create2(port=port, baud=baud['default'])
bot.start()
bot.safe()

def getClosestTag():
    rootationCounter = 0
    while ( True ) :
        print("START READ:")
        tags = reader.read()
        tags.sort(key = lambda x: abs(x.rssi) ) 
        for i in range (len(tags)):
            tag = tags[i] 
            if getTagName(tag) in total_tags_names:
                print( getTagLabel(tag) , tag.rssi  )
                if (getTagName(tag) not in identified_tags) :
                    return tag
        ## EXPLORE - rotates to discover tags
        print("SEARCHING, ROTATION #", rootationCounter)
        bot.drive_direct(100, 0)
        time.sleep(2)
        bot.drive_stop()
        time.sleep(2)
        rootationCounter += 1
        if ( rootationCounter == 8 ):
            return -1

def getTagName(tag):
    return str(tag.epc)[2:-1]

def getTagLabel(tag):
    return tag_dictionary[getTagName(tag)]

while (True):
    #synchronous reading
    #have not tested
    
    print("Identified tags:" , identified_tags)
    print("Tags Left" , total_tags_names - identified_tags)
    closest_tag = getClosestTag()
    #move 90 degrees to search for a tag
    if (len(identified_tags) == len(total_tags_names)) :
        break
    if closest_tag == -1 :
        bot.drive_direct(100, 100)
        time.sleep(2)
        bot.drive_stop()
        continue
    wanted_tag = closest_tag
    if abs( closest_tag.rssi ) <= 55 :
        # just check if the tag has been discovered already
        if ( getTagName(closest_tag) not in identified_tags ) :
            ## have robot behavior --> found tag
            bot.drive_direct(-100, -100)
            print("FOUND: ", getTagName(closest_tag), getTagLabel(closest_tag), closest_tag.rssi)
            identified_tags.add( getTagName(closest_tag) )
            tags_left = total_tags_names - identified_tags
            print("TAGS LEFT:", len(tags_left))
            # gets a random tag from our wanted set
            wanted_tag = r.sample(tags_left, 1) [0]
            # clean for some amount of time
            # TODO code for cleaning around the RFID Tag
    else :
        ## FNDS A TAG -> not in range, tries to get closer
        previous_reading = abs(closest_tag.rssi)
        # TODO do some sort of reading and moving until the rssi goes up
        bot.drive_direct(100, 100)
        time.sleep(0.5)
        old_tag = closest_tag
        closest_tag = getClosestTag()
        post_reading = abs(closest_tag.rssi)
        if (closest_tag == old_tag) :
            pass
        else:
            # tag changed? make sure dont move
            bot.drive_stop()
            time.sleep(1)
            closest_tag = getClosestTag()
        

        delta = post_reading - previous_reading
        # positive delta means new reading is worst than old reading, therefore rotate CCW
        if delta > 0 :
            #might be last time to rotate right so drive forward somehow
            # TODO rotate left
            # TODO command to rotate for some amount of seconds
            bot.drive_direct(50, 0)
            time.sleep(2)
            bot.drive_stop()
        else :
            #rotate right some more to get more readings
            #TODO rotate right
            #TODO command to rotate for some amount of seconds
            bot.drive_direct(50, 0)
            time.sleep(2)
            bot.drive_stop()
            pass


print("Done")
#clean up one last time??

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
