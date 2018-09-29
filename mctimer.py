import mcrcon
import datetime
from time import sleep
from random import randint

# python 2 compatibility
try: input = raw_input
except NameError: pass

#
# Change these variables to suit your setup:
#
# 1. Which user should this script be monitoring?
user = "EnAmalia"
# 2. How many minutes per day should he/she be allowed to play on the servers?
allowance_per_day = 60
# 3. At what IPs can we find the servers, and on what ports is RCON running? (*)
servers = [ ("192.168.0.121", 25575, "sporklift"), ("192.168.0.121", 25576, "sporklift") ]
#
# End of user-configurable stuff
#
#
# (*) See https://github.com/ragnarlonn/mctimer/readme.md for info on how to 
#     configure your Minecraft servers, and enable RCON on them
#

# Some globals
normal_check_interval = 60
timeout_check_interval = 10
annoying_sounds = [
    "entity.donkey.angry",
    "entity.cat.ambient",
    "entity.chicken.ambient",
    "entity.pig.ambient",
    "entity.cow.ambient",
    "entity.donkey.ambient",
    "entity.horse.ambient",
    "entity.mule.ambient",
    "entity.sheep.ambient"
]

def update_bossbar(rcon, percentage):
    # Do we have a bossbar here?
    response = rcon.command("/bossbar list")
    if response.find("Time left") == -1:
        rcon.command("/bossbar add %s \"Time left\"" % "amaliatimer")
    rcon.command("/bossbar set amaliatimer style notched_10")
    rcon.command("/bossbar set amaliatimer max 10")
    rcon.command("/bossbar set amaliatimer value %d" % int((9 + percentage) / 10))
    rcon.command("/bossbar set amaliatimer players @a")
    if percentage <= 0:
        if randint(0,4) == 0:
            rcon.command("/effect give %s nausea %d" % (user, timeout_check_interval))
            for i in range(3):
                sound = annoying_sounds[randint(0,len(annoying_sounds)-1)]
                rcon.command("/playsound %s ambient %s ~ ~ ~ 1.0 2.0 1.0" % (sound, user))
                sleep(0.5)
        else:
            rcon.command("/playsound entity.player.levelup neutral %s ~ ~ ~ 1.0 1.0 1.0" % user)
        rcon.command("/title %s title {\"text\":\"Time to stop!\",\"bold\":true}" % user)
    elif percentage % 10 == 0:
        if percentage >= 30:
            rcon.command("/playsound entity.cat.purreow ambient @a ~ ~ ~ 0.8 1.0 0.8")
        else:
            rcon.command("/playsound entity.cat.purreow ambient @a ~ ~ ~ 1.0 1.2 1.0")

def reconnect(servers):
    rcons = []
    for server in servers:
        host, port, password = server
        r = mcrcon.MCRcon()
        print("# connecting to %s:%i..." % (host, port))
        r.connect(host, port, password)
        r.command("/gamerule sendCommandFeedback false")
        rcons.append(r)
    return rcons

def main(servers):
    rcons = reconnect(servers)
    curday = -1

    while True:
        now = datetime.date.today()
        if now != curday:
            # Start new timer
            time_left = allowance_per_day
            curday = now
        if time_left <= 0:
            sleep(timeout_check_interval)
        else:
            sleep(normal_check_interval)
        # Check if Amalia is logged on
        logged_on = False
        print "Looking for %s on servers..." % user
        try:
            for i in range(len(rcons)):
                response = rcons[i].command("/list")
                if response.find(user) != -1:
                    print "   Found %s on server %s:%d" % (user, servers[i][0], servers[i][1])                    
                    # Subtract a minute
                    time_left -= 1
                    print "   Time left: %d" % time_left
                # Update bossbar
                update_bossbar(rcons[i], int((time_left * 100) / allowance_per_day))
        except:
            print "Lost connection to server(s), trying to reconnect..."
            for i in range(len(rcons)):
                rcons[i].disconnect()
            rcons = reconnect(servers)


if __name__ == '__main__':
    main(servers)
