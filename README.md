<p align="center"><img src="screenshot.png" alt="mctimer" width="400" height="300"></p>

# mctimer

#### Limit the amount of time your kid(s) spend playing Minecraft on your local Minecraft servers

This is a tiny Python app that monitors one or multiple Minecraft servers that you control. It will scan
the servers repeatedly to see if a certain, specified user is logged on or not and if they are, time will
be deducted from a daily allowance. When the allowance is spent for the day, the app will start displaying
large "Time is up!" messages to the user, together with sound effects.

Dependencies
------------

The app uses the [RCON](http://wiki.vg/RCON) protocol to talk to the Minecraft servers. This means you have to have RCON enabled, 
and also the [MCRcon](https://github.com/barneygale/MCRcon) Python library installed. It's very simple though - just follow the steps below.

Getting started
---------------

- Install MCRcon. On a Mac: 
```
    git clone https://github.com/barneygale/MCRcon
    cd MCRcon
    sudo python setup.py install
```

- Edit your server.properties file and change `enable-rcon=false` to `enable-rcon=true`

- Add the following lines to your server.properties file:
```
    rcon.port=25575
    rcon.password=yourverysecretpassword
```

- Edit mctimer.py and change these definitions at the beginning of the file:
```
    user="EnAmalia"
    allowance_per_day = 90
    servers = [ ("192.168.0.121", 25575, "sporklift"), ("192.168.0.121", 25576, "sporklift") ]
    #
    # The first is the name of the Minecraft user you want to time limit
    #
    # The second is the number of minutes per day the user should be allowed to play
    #
    # The third is a list of all Minecraft servers where the user should be time limited
    # (note that you need to be in control of those servers; you can't use mctimer to limit time
    #  on public servers somewhere out on the Internet)
    # 
    # Each server is specified as a 3-tuple containing (IP, port, password). The port number and password are
    # whatever you configured RCON to use in step 3 above (`rcon.port=...` and `rcon.password=...`)
    #
```
