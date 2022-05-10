from ast import Pass
from logging.handlers import RotatingFileHandler
import mercury
#From this library https://github.com/gotthardp/python-mercuryapi
from  pycreate2 import Create2
#From this library https://github.com/MomsFriendlyRobotCompany/pycreate2
import time
import random as r
#ls on dev and choose cu.usbmodemXXXXXX
reader = mercury.Reader("tmr:///dev/cu.usbmodem141301")
reader.set_region("EU3")
reader.set_read_plan([4], "GEN2")

#afdgb
#abdfg
# RFID Tag Names Names
# {300833B2DDD9014000000000 , E28011700000020A7B2E8D44, E200001D5607014724307EB8 , E28011700000020F4CB328F0, 
# E2004740D42BFE4A755E1887, E2000020780A003117906133, E2801170000002118067C4E5, E20043B7034FB3891A4627D1}

#dict might be useful to map name to RSSI? not too sure tho 
# tag_dictionary = {'E2004740D42BFE4A755E1887': 'A', 'E28011700000020F4CB328F0':'B', 'E200001D5607014724307EBD':'C', '300833B2DDD9014000000000':'D', \
#     'E2801170000002118067C4E5':'E', 'E20043B7034FB3891A4627D1':'F', 'E2000020780A003117906133':'G', 'E28011700000020A7B2E8D44':'H'}
# tag_dictionary_misses = {'E2004740D42BFE4A755E1887': 0, 'E28011700000020F4CB328F0': 0, 'E200001D5607014724307EBD': 0, '300833B2DDD9014000000000': 0, \
#     'E2801170000002118067C4E5': 0, 'E20043B7034FB3891A4627D1': 0, 'E2000020780A003117906133': 0, 'E28011700000020A7B2E8D44': 0}
total_tags_names, identified_tags  = set() , set()
# ordered ABC from our sticky notes, A-H
# total_tags_names = {'E2004740D42BFE4A755E1887' , 'E28011700000020F4CB328F0', '300833B2DDD9014000000000', \
#     'E20043B7034FB3891A4627D1', 'E2000020780A003117906133' }
tag_dictionary = {'E2004740D42BFE4A755E1887': 'A', 'E28011700000020F4CB328F0':'B', '300833B2DDD9014000000000':'D', \
 'E20043B7034FB3891A4627D1':'F', 'E2000020780A003117906133':'G' }
tag_dictionary_misses = {'E2004740D42BFE4A755E1887': 0, 'E28011700000020F4CB328F0': 0, '300833B2DDD9014000000000': 0, \
    'E20043B7034FB3891A4627D1': 0, 'E2000020780A003117906133': 0}
total_tags_names = {'E2004740D42BFE4A755E1887' , 'E28011700000020F4CB328F0', '300833B2DDD9014000000000', \
    'E20043B7034FB3891A4627D1', 'E2000020780A003117906133'}
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

def getClosestTag(ignore = []):
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
    print("Identified tags:" , identified_tags)
    print("Tags Left" , total_tags_names - identified_tags)
    closest_tag = getClosestTag()
    #Done with scanning
    if (len(identified_tags) == len(total_tags_names)) :
        break
    
    if closest_tag == -1 :
        # bot.drive_direct(-100, -100)
        time.sleep(1)
        bot.drive_stop()
        continue

    wanted_tag = closest_tag
    print ("Going After: ", getTagLabel(wanted_tag))
    while (True):
        print("RSSI: ", wanted_tag.rssi)
        if abs( wanted_tag.rssi ) <= 49 :
            #Tag found
            if ( getTagName(closest_tag) not in identified_tags ) :
                #(250,125) (200,100)
                bot.drive_direct(-200, -200)
                time.sleep(2)
                bot.drive_direct(-100, -200)
                time.sleep(2)
                print("FOUND: ", getTagName(closest_tag), getTagLabel(closest_tag), closest_tag.rssi)
                identified_tags.add( getTagName(closest_tag) )
                tags_left = total_tags_names - identified_tags
                print("TAGS LEFT:", len(tags_left))
                break
        else :
            ## FINDS A TAG -> not in range, tries to get closer
            previous_reading = abs(wanted_tag.rssi)
            bot.drive_direct(100, 100)
            time.sleep(0.5)
            tags = reader.read()
            for i in range(len(tags)):
                if getTagName(tags[i]) == getTagName(wanted_tag) :
                    cond = False
                    # print ("tag was found")
                    wanted_tag = tags[i]
                    break
                else:
                    cond = True
            # New tag has to be claimed because old one is out of range.
            if cond and i == len(tags) - 1: 
                print ("tag was not found, no Delta")
                desired_tag = getTagName(wanted_tag)
                tag_dictionary_misses[desired_tag] += 1
                print(tag_dictionary_misses)
                break

            post_reading = abs(wanted_tag.rssi)
            delta = post_reading - previous_reading
            # positive delta means new reading is worst than old reading, therefore rotate CCW
            sensors = bot.get_sensors()
            sensors.wall == sensors[1]  # True
            if (sensors.wall) :
                bot.drive_direct(-300, -300)
                time.sleep(1)
                bot.stop()
                bot.drive_direct(-150, 150)
                time.sleep(.5)
                bot.stop()

            while (delta ==  0):
                delta = r.randint(-1 , 1)
            if delta > 0 :
                print("Delta > 0 ", delta)
                #rotate left some more to get more readings
                if abs(delta) > 2 :
                    bot.drive_direct(45, 0)
                elif abs(delta) > 4 :
                    bot.drive_direct(80, 0)
                elif abs(delta) > 8 :
                    bot.drive_direct(120, 0)
                time.sleep(2)
                bot.drive_stop()
            elif delta < 0 :
                print("Delta < 0", delta)
                #rotate right some more to get more readings
                if abs(delta) > 2 :
                    bot.drive_direct(0, 45)
                elif abs(delta) > 4 :
                    bot.drive_direct(0, 80)
                elif abs(delta) > 8 :
                    bot.drive_direct(0, 120)
                time.sleep(2)
                bot.drive_stop()

print("Done")