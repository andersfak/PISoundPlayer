#!/usr/bin/python
from datetime import datetime
import time
import os

schema_path = "/media/pi/SOUND/"
sound_path = "/media/pi/SOUND/Meddelanden/"

schemaFile = open(schema_path + 'schema.txt', 'r')

line = schemaFile.readline()
season = line
schema = []
while True:
    line = schemaFile.readline()
    
    if not line:
        break
    else:
        line = line.replace("monday","0").replace("tuesday","1").replace("wednesday","2").replace("thursday","3").replace("friday","4").replace("saturday","5").replace("sunday","6")
        schema.append(line.strip())


schemaFile.close()

excFile = open(schema_path + 'exceptions.txt', 'r')

exceptions = []
while True:
    line = excFile.readline()
    
    if not line:
        break
    else:
        exceptions.append(line.strip())
excFile.close()

now = datetime.now()
date = datetime.date(now)
today = datetime.today().weekday()
exceptionDate = ""

# main loop

while True:
    now = datetime.now()
    tmpTime = now.time()
    tmpHour = tmpTime.hour
    if season == "summer":
        tmpHour = tmpHour-1
    
    currentTime = str(str(tmpHour) + ":" + str(tmpTime.minute))
    today = str(datetime.date(now))
    currentWeekday = str(datetime.today().weekday())

    soundPlayed = False

    # Kolla undantagslistan först:
    for line in exceptions:
        
        details = line.split(",")

        dateToCheck = details[0]
        timeToCheck = details[1]
        soundToPlay = details[2]

        if dateToCheck == today:
            exceptionDate = today
            if timeToCheck == currentTime:


                os.system("aplay " + sound_path + soundToPlay)
                soundPlayed = True
                time.sleep(60)



    # Normal-schemat:
    if soundPlayed == False and exceptionDate != today:

        for line in schema:

            details = line.split(",")

            dayToCheck = details[0]
            timeToCheck = details[1]
            soundToPlay = details[2]

            if dayToCheck == currentWeekday:
                if timeToCheck == currentTime:
                    
                    os.system("aplay " + sound_path + soundToPlay)
                    soundPlayed = True
                    time.sleep(60)


    
    time.sleep(20)
